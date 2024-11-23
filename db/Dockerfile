# Используем официальный образ PostgreSQL
FROM postgres:15

# Копируем SQL-скрипты для инициализации базы
COPY init.sql /docker-entrypoint-initdb.d/

# Устанавливаем переменные окружения для автоматического создания базы данных
ENV POSTGRES_USER=admin
ENV POSTGRES_PASSWORD=adminpassword
ENV POSTGRES_DB=weather_history

# Открываем стандартный порт PostgreSQL
EXPOSE 5432