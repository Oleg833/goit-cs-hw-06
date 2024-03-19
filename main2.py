from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import socket
import threading
import pymongo
from datetime import datetime
import json
import signal
from pymongo import MongoClient
from connect_db import create_connect

# client = create_connect()
# db = client["mydatabase"]
# collection = db["messages"]

PORT = 3000
PORT2 = 5000


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            with open("index.html", "rb") as file:
                self.wfile.write(file.read())
        elif self.path == "/message.html":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            with open("message.html", "rb") as file:
                self.wfile.write(file.read())
        elif self.path == "/logo.png":
            self.send_response(200)
            self.send_header("Content-type", "image/png")
            self.end_headers()
            with open("logo.png", "rb") as file:
                self.wfile.write(file.read())
        elif self.path == "/style.css":
            self.send_response(200)
            self.send_header("Content-type", "text/css")
            self.end_headers()
            with open("style.css", "rb") as file:
                self.wfile.write(file.read())
        else:
            self.send_error(404, "File Not Found")

    def do_POST1(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length).decode("utf-8")

        # Розбираємо дані POST-запиту
        parsed_data = urllib.parse.parse_qs(post_data)
        username = parsed_data.get("username", [""])[0]
        message = parsed_data.get("message", [""])[0]

        print(f"Received data: username={username}, message={message}")

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Data received")

    def do_POST(self):
        if self.path == "/message":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            # Розбираємо дані POST-запиту
            parsed_data = urllib.parse.parse_qs(post_data.decode("utf-8"))
            username = parsed_data.get("username", [""])[0]
            message = parsed_data.get("message", [""])[0]

            print(f"Received data: username={username}, message={message}")

            # Відправка даних на Socket-сервер
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect(("localhost", PORT2))
                sock.sendall(post_data)
                # sock.sendall(b"Hello, world")

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Data sent to socket server")


# Запуск веб-сервера
def run_server():
    server_address = ("", PORT)
    httpd = HTTPServer(server_address, RequestHandler)
    print(f"Starting server on port {PORT}...")
    httpd.serve_forever()


# Запуск сокет-сервера
def socket_server1(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("localhost", port))
        s.listen()
        print(f"Сокет сервер слухає порт {PORT2}")
        conn, addr = s.accept()
        with conn:
            print(f"Підключено {addr}")
            while True:
                data = conn.recv(1024).decode("utf-8")
                if not data:
                    break
                try:
                    # Конвертація отриманих даних у словник
                    data_dict = json.loads(data)

                    # Підключення до MongoDB і вставка даних
                    client = create_connect()
                    db = client["db-messages"]
                    collection = db["messages"]

                    post = {
                        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "username": data_dict.get("username"),
                        "message": data_dict.get("message"),
                    }
                    print(post)
                    # Спроба зберегти дані в MongoDB
                    collection.insert_one(post)
                    print("Повідомлення збережено в MongoDB")
                except (json.JSONDecodeError, pymongo.errors.PyMongoError) as e:
                    print(f"Помилка при обробці даних: {e}")
                except Exception as e:
                    print(f"Виникла помилка: {e}")
                # finally:
                #     connection.close()


def handle_client(connection, address):
    print(f"Підключення з {address} встановлено")

    # Створення буфера для збору даних
    data_buffer = ""

    try:
        # Отримання даних від клієнта
        while True:
            data = connection.recv(1024).decode("utf-8")
            if not data:
                break
            data_buffer += data

            # Конвертація отриманих даних у словник
            data_dict = json.loads(data_buffer)

            # Підключення до MongoDB і вставка даних
            client = create_connect()
            # client = MongoClient("localhost", 27017)
            db = client["db-messages"]
            collection = db["messages"]

            post = {
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "username": data_dict.get("username"),
                "message": data_dict.get("message"),
            }

            collection.insert_one(post)
            print("Повідомлення збережено в MongoDB")
    except Exception as e:
        print(f"Виникла помилка: {e}")
    finally:
        connection.close()


def socket_server(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("", port))
    server.listen()
    print(f"Socket сервер слухає на порту {port}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


# Функція для зупинки серверів
def stop_servers(signum, frame):
    global server_running
    print("Stopping servers...")
    server_running = False


# Додамо обробник для сигналу завершення роботи (CTRL+C)
signal.signal(signal.SIGINT, stop_servers)

if __name__ == "__main__":
    # Запускаємо веб-сервер у окремому потоці
    web_thread = threading.Thread(target=run_server)
    web_thread.start()

    # Запускаємо сокет-сервер у головному потоці
    socket_server(PORT2)
