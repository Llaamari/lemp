#!/usr/bin/env python3
import os
import requests
import mysql.connector
from datetime import datetime

# Read API key from environment variable (or placeholder in GitHub)
API_KEY = os.getenv("OPENWEATHER_API_KEY", "YOUR_API_KEY_HERE")

CITY = "Oulu"
URL = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

def main():
    try:
        response = requests.get(URL, timeout=10)
        data = response.json()

        # Validate response
        if "main" not in data:
            print("Error: Unexpected API response:", data)
            return

        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        timestamp = datetime.now()

        # Connect to database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",             # Use real password only on server
            database="weather_db"
        )

        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS weather_data (
                id INT AUTO_INCREMENT PRIMARY KEY,
                city VARCHAR(50),
                temperature FLOAT,
                description VARCHAR(100),
                timestamp DATETIME
            )
        """)

        cursor.execute("""
            INSERT INTO weather_data (city, temperature, description, timestamp)
            VALUES (%s, %s, %s, %s)
        """, (CITY, temp, desc, timestamp))

        conn.commit()
        cursor.close()
        conn.close()

        print(f"Saved: {CITY} {temp}°C {desc} at {timestamp}")

    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    main()