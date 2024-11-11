from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import FAISS
from backend.ai_func.genai import get_conversation_chain
from dotenv import load_dotenv
import os

load_dotenv()

embeddings = GoogleGenerativeAIEmbeddings(google_api_key= os.getenv('GOOGLE_API_KEY'),
                             model = 'models/embedding-001')

def get_chunks(text):
    splitter = RecursiveCharacterTextSplitter(chunk_size = 3000,
                                   chunk_overlap = 250)
    return splitter.split_text(text)

def get_vector_storage(text_chunks):
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")


def user_input(query):
    
    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization= True)
    docs = new_db.similarity_search(query)

    chain = get_conversation_chain()

    
    response = chain(
        {"input_documents":docs, 
         "question": query}, 
         return_only_outputs=True)

    return response["output_text"]  
