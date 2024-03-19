import socket
import os
from pathlib import Path
import threading
from pymongo import MongoClient
from datetime import datetime
import json
import logging
import urllib.parse
import pymongo
from connect_db import create_connect
from dotenv import load_dotenv

logging.basicConfig(
    filename="server.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
# Флаг для зупинки сервера
server_running = True


def handle_client(connection, address):
    print(f"Підключення з {address} встановлено")

    try:
        while True:
            data = connection.recv(1024).decode("utf-8")
            if not data:
                break
            # Розпарсити дані форми у словник
            parsed_data = urllib.parse.parse_qs(data)
            # Видалити \r\n з значення ключа 'message'
            if "message" in parsed_data:
                parsed_data["message"] = [
                    parsed_data["message"][0].strip().replace("\r\n", " ")
                ]
            username = parsed_data.get("username", [""])[0]
            message = parsed_data.get("message", [""])[0]
            # print(f"Received data: username={username}, message={message}")

            # Підключення до MongoDB і вставка даних
            client = create_connect()
            db = client["db-messages"]
            collection = db["messages"]

            post = {
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "username": username,
                "message": message,
            }
            print(post)

            collection.insert_one(post)
            print("Повідомлення збережено в MongoDB")
    except Exception as e:
        logging.error(f"Помилка при обробці даних: {e}")

    finally:
        connection.close()


def socket_server(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("", port))
    server.listen()
    global server_running
    try:
        print(f"Starting socket server on port {port}")
        while server_running:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
    except KeyboardInterrupt:
        logging.error("Server stoping...")
        server_running = False
    finally:
        server.close()


if __name__ == "__main__":

    ENV_PATH = Path(__file__).parent / ".env"

    load_dotenv(ENV_PATH)

    PORT2 = int(os.getenv("PORT2"))
    socket_server(PORT2)
