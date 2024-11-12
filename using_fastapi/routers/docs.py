from fastapi import APIRouter, UploadFile, File, Response, HTTPException, status
from backend.ai_func.genai import start_conversation
import uuid
from backend.db.qdrant_storage import QdrantStorage
from backend.processor.docs_preprocessing import get_text
from typing import List

router = APIRouter(
    prefix='/pdf',
    tags = ['test'],
    responses={404:{'description': 'Internal Server Error.'}}
)

@router.post('/upload_files/')
async def upload_pdf(files: List[UploadFile] = File(...)):
    
    text = get_text(files)

    if not text:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= 'Not able to process the file')
    
    session_id = str(uuid.uuid4())
    qdrant_storage = QdrantStorage(session_id)
    if not qdrant_storage:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= 'Not able to access Qdrant Storage.')
    
    results = qdrant_storage.store_media_text(text)
    if not results:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= 'Not able to store the data in QdrantStorage.')

    return {'session_id': session_id,
            'message': results['message']}

@router.post('/chat_from_the_document')
async def search_in_pdf(session_id, query):
    
    qdrant_storage = QdrantStorage(session_id)
    if not qdrant_storage:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= 'Not able to access Qdrant Storage.')
    
    results = qdrant_storage.retrieve_similar(query)
    if not results:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= 'Not able to fetch the data from QdrantStorage.')
    
    response = start_conversation(query, results)
    if not response:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= 'Not able to generate the response from AI.')

    return Response(content= str(response))