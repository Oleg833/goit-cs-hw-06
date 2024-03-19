import http.server
import os
import threading
from dotenv import load_dotenv
from pathlib import Path

WEB_DIR = "./front-init"  # Шлях до вашої папки з веб-контентом
ENV_PATH = Path(__file__).parent / ".env"

load_dotenv(ENV_PATH)

PORT = int(os.getenv("PORT"))


class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Встановлення базової директорії для статичних файлів
        self.directory = WEB_DIR
        # Перевірка на існування файлу
        if not os.path.exists(os.path.join(WEB_DIR, self.path[1:])):
            self.path = "error.html"

        # Обробка запиту
        return http.server.SimpleHTTPRequestHandler.do_GET(self)


# Налаштування обробника HTTP запитів
handler_object = MyHttpRequestHandler


# Функція для запуску веб-сервера
def run_server(port):
    httpd = http.server.HTTPServer(("", port), handler_object)
    try:
        print("Сервер стартував на порту", port)
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Сервер зупинено")
        httpd.shutdown()


if __name__ == "__main__":
    # Запускаємо веб-сервер у окремому потоці
    web_thread = threading.Thread(target=run_server, args=(PORT,))
    web_thread.start()
