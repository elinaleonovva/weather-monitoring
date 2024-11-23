-- Проверяем, существует ли база данных, если нет — создаём
DO $$
BEGIN
   IF NOT EXISTS (
       SELECT FROM pg_database WHERE datname = 'weather_history'
   ) THEN
       CREATE DATABASE weather_history;
   END IF;
END
$$;

-- Подключаемся к базе данных
\c weather_history;

-- Проверяем, существует ли таблица history, если нет — создаём
DO $$
BEGIN
   IF NOT EXISTS (
       SELECT FROM information_schema.tables
       WHERE table_name = 'history'
   ) THEN
       CREATE TABLE history (
           id SERIAL PRIMARY KEY,
           city VARCHAR(100) NOT NULL,
           temperature REAL NOT NULL,
           condition VARCHAR(100) NOT NULL,
           timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
       );
   END IF;
END
$$;
