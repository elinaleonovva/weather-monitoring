# Используем официальный образ Python
FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    libpq-dev gcc && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта в контейнер
COPY server.py /app/
COPY requirements.txt /app/

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Указываем переменные окружения
ENV WEATHER_API_KEY=your_api_key_here

# Открываем порт 5000
EXPOSE 5000

# Запускаем приложение
CMD ["python", "server.py"]