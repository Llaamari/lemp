#!/usr/bin/env python3
import requests
import mysql.connector
from datetime import datetime

URL = "https://api.frankfurter.app/latest?from=EUR"

def main():
    try:
        response = requests.get(URL, timeout=10)
        data = response.json()

        if "rates" not in data:
            print("Error: Unexpected API response:", data)
            return

        base = "EUR"
        timestamp = datetime.now()

        # Connect to database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="finance_db"
        )

        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS exchange_rates (
                id INT AUTO_INCREMENT PRIMARY KEY,
                base VARCHAR(10),
                currency VARCHAR(10),
                rate FLOAT,
                timestamp DATETIME
            )
        """)

        for currency, rate in data["rates"].items():
            cursor.execute("""
                INSERT INTO exchange_rates (base, currency, rate, timestamp)
                VALUES (%s, %s, %s, %s)
            """, (base, currency, float(rate), timestamp))

        conn.commit()
        cursor.close()
        conn.close()

        print("Exchange rates updated at:", timestamp)

    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    main()