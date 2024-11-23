from flask import Flask, request, jsonify
import requests
import os
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

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

# API Key для WeatherAPI (используем переменные окружения для безопасности)
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
WEATHER_API_URL = "http://api.weatherapi.com/v1/current.json"

# URL для сервиса истории запросов (подключение к сервису в Docker)
HISTORY_SERVICE_URL = "http://localhost/add/"  # Убедитесь, что название сервиса совпадает с docker-compose.yml

@app.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "City is required"}), 400

    try:
        # Отправка запроса к weatherapi.com
        response = requests.get(
            WEATHER_API_URL,
            params={"key": WEATHER_API_KEY, "q": city, "aqi": "no"}
        )
        if response.status_code != 200:
            return jsonify({"error": response.json().get("error", {}).get("message", "Unknown error")}), 400

        data = response.json()

        # Формируем ответ с информацией о погоде
        weather_info = {
            "city": data["location"]["name"],
            "temperature": data["current"]["temp_c"],
            "condition": data["current"]["condition"]["text"]
        }

        # Отправляем информацию в сервис истории запросов
        try:
            add_to_history(weather_info)
        except Exception as e:
            return jsonify({
                "error": "Weather data fetched successfully, but failed to connect to history service.",
                "details": str(e)
            }), 500

        return jsonify(weather_info)

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to fetch weather data: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

def add_to_history(data):
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
