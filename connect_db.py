import os
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
from pathlib import Path
from pymongo import MongoClient
from datetime import datetime

# # Підключення до MongoDB
# client = MongoClient("localhost", 27017)
# db = client["messages_db"]
# collection = db["messages"]

# # Вставка документа
# post = {"date": datetime.now(), "username": "user", "message": "Hello"}
# collection.insert_one(post)


############
ENV_PATH = Path(__file__).parent / ".env"


def create_connect() -> MongoClient:
    load_dotenv(ENV_PATH)

    client = MongoClient(
        os.getenv("MONGO_DB_HOST"),
        server_api=ServerApi("1"),
    )

    return client


if __name__ == "__main__":
    client = create_connect()
    db = client["db-messages"]
    collection = db["messages"]
    cats = collection.find()
    for cat in cats:
        print(cat)
