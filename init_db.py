from pymongo import MongoClient
from datetime import datetime

import pymongo


def initialize_database():
    try:
        client = MongoClient("mongodb://localhost:27017/")
        db = client["db-messages"]
        users_collection = db["messages"]

        init_post = [
            {
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "username": "John Doe",
                "message": "message from John Doe",
            },
            {
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "username": "Jane Smith",
                "message": "message from Jane Smith",
            },
        ]

        users_collection.insert_many(init_post)
        print("Database initialized successfully!")
    except pymongo.errors.PyMongoError as e:
        print(f"An error occurred: {e}")
    return client


if __name__ == "__main__":
    client = initialize_database()
    db = client["db-messages"]
    collection = db["messages"]
    cats = collection.find()
    for cat in cats:
        print(cat)
