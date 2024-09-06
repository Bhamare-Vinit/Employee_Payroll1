from fastapi import FastAPI
from src.routes import router
from dotenv import load_dotenv
from pymongo import MongoClient
from contextlib import asynccontextmanager
import os

load_dotenv(dotenv_path='.env_variable')

@asynccontextmanager
async def lifespan(app: FastAPI):
    mongo_uri = os.getenv("MONGO_URI")
    print("Database Initializing",mongo_uri)
    app.mongodb_client = MongoClient(mongo_uri)
    app.database = app.mongodb_client["fastapi"]
    app.collection = app.database["Crud"]
    print("Database Connected")
    
    yield
    

    app.mongodb_client.close()
    print("Database Disconnected")


app = FastAPI(lifespan=lifespan)
app.include_router(router)
