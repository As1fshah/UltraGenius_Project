import uuid
from datetime import datetime
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from qdrant_client import QdrantClient, models
import os
from dotenv import load_dotenv
from qdrant_client.http.models import MatchValue, FieldCondition, Filter,PointStruct
from langchain.text_splitter import RecursiveCharacterTextSplitter

load_dotenv()

qdrant_client = QdrantClient(url=os.getenv('QDRANT_URL'), api_key=os.getenv('QDRANT_API_KEY'))

collection_name = os.getenv("QDRANT_COLLECTION_NAME")

def create_collection():
    if not qdrant_client.collection_exists(collection_name=collection_name):
        qdrant_client.create_collection(
            collection_name,
            vectors_config=models.VectorParams(size=768, distance=models.Distance.COSINE)
        )
        print("Qdrant collection created")
    print(f"Qdrant collection '{collection_name}' in use")

def get_embeddings(text):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    return embeddings.embed_query(text)

def get_chunks(text):
    text = text.strip()
    splitter = RecursiveCharacterTextSplitter(chunk_size = 3000, chunk_overlap = 150)
    chunks = splitter.split_text(text)
    return chunks

def get_chunks_embeddings(chunks):
    embeded_chunks_index = []
    for chunk in chunks:
        embeded_chunks_index.append(get_embeddings(chunk))
    return embeded_chunks_index


class QdrantStorage:
    def __init__(self, session_id):
        self.session_id = session_id
        self.id_query = str(uuid.uuid4())
        self.id_response = str(uuid.uuid4())

    def retrieve_similar(self, query):
        try:
            embedding = get_embeddings(query)
            results = qdrant_client.search(
                collection_name=collection_name,
                query_vector=embedding,
                limit=2,
                query_filter=Filter(must=[
                    FieldCondition(
                        key="session_id",
                        match=MatchValue(value=self.session_id)
                    )
                ])
            )
            for res in results:
                print(res.score)
            chat_history = [(res.payload['text'], res.payload['type']) for res in results]

            return chat_history
        except Exception as e:
            print(str(e))
            return []

    def store_media_text(self, text):
        try:
            text_chunks = get_chunks(text)
            embeddings = get_chunks_embeddings(text_chunks)
            points = []
            for text_chunk, embedding in zip(text_chunks, embeddings):
                points.append(
                    PointStruct(id=str(uuid.uuid4()), vector=embedding, payload={
                        "session_id": self.session_id,
                        "text": text_chunk,
                        "type": "Media Text",
                        'timestamp': datetime.now()
                    }),
                )
            qdrant_client.upsert(
                collection_name=collection_name,
                wait=True,
                points=points
            )
            return {"is_success": True, "message": "Media Text added to vector db successfully"}
        except Exception as e:
            return {"is_success": False, "message": str(e)}