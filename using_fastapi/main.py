from fastapi import FastAPI
import os
from dotenv import load_dotenv
from backend.db.qdrant_storage import create_collection
from routers import docs

load_dotenv()
app = FastAPI()

create_collection()
app.include_router(docs.router)