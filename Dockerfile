# Використовуємо офіційний образ Python версії 3.x
FROM python:3.10

# Встановлюємо необхідні пакети за допомогою pip
RUN pip install pymongo

# Встановлюємо MongoDB
RUN apt-get update && apt-get install -y \
    mongodb \
 && rm -rf /var/lib/apt/lists/*

# Створюємо робочу директорію та копіюємо файли додатку в неї
WORKDIR /app
COPY . /app

# Команда для запуску додатку при старті контейнера
CMD ["python", "main.py"]
