from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# Параметры подключения к базе данных
DB_HOST = "db"  # Имя сервиса из docker-compose.yml
DB_NAME = "weather_history"
DB_USER = "admin"
DB_PASSWORD = "adminpassword"


def get_db_connection():
    """Функция для подключения к базе данных."""
    return psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )


def init_db():
    """Инициализация базы данных: создание таблицы, если её нет."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id SERIAL PRIMARY KEY,
            city VARCHAR(100) NOT NULL,
            temperature REAL NOT NULL,
            condition VARCHAR(100) NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        conn.commit()
        cursor.close()
        conn.close()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Error initializing database: {e}")


# Инициализация базы данных при старте сервера
init_db()


# Маршрут для добавления записи в историю
@app.route('/add', methods=['POST'])
def add_to_history():
    data = request.json
    city = data.get("city")
    temperature = data.get("temperature")
    condition = data.get("condition")

    if not all([city, temperature, condition]):
        return jsonify({"error": "City, temperature, and condition are required"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO history (city, temperature, condition)
        VALUES (%s, %s, %s)
        """, (city, temperature, condition))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Record added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Маршрут для получения всей истории
@app.route('/history', methods=['GET'])
def get_history():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT city, temperature, condition, timestamp FROM history ORDER BY timestamp DESC LIMIT 5")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(rows)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
