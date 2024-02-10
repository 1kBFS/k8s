import os

from fastapi import FastAPI
from pymongo import MongoClient

from routes import router

app = FastAPI()


@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(os.getenv("URL", "localhost"))
    app.database = app.mongodb_client[os.getenv("DB_NAME", "facts")]
    print("Connected to the MongoDB database!")


@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()


@app.get("/")
def say_hello():
    return {"message": f"Hello, use /docs to get help!"}


app.include_router(router=router, tags=["facts"], prefix="/fact")
