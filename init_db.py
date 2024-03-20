from pymongo import MongoClient
from datetime import datetime


def initialize_database():
    # Підключення до MongoDB
    client = MongoClient("mongodb://localhost:27017/")
    db = client["db-messages"]
    users_collection = db["messages"]

    print("Database initialized successfully!")

    # Ініціалізація даних
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

    # Вставка даних до колекції
    users_collection.insert_many(init_post)


if __name__ == "__main__":
    # Виклик функції для ініціалізації бази даних
    initialize_database()
