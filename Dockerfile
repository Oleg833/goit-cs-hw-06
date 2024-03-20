# Використовується офіційний образ Python як базовий
FROM python:3.11-slim

# Встановлення робочого каталогу в контейнері
WORKDIR /app

# Копіювання файлів в робочий каталог
COPY . /app

# Встановлення Python залежностей
RUN pip install --no-cache-dir -r requirements.txt

# Відкриття портів
EXPOSE 3000
EXPOSE 5000

# Команда для запуску скрипта
CMD ["python", "main.py"]