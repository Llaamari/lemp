#!/usr/bin/env python3
"""
MQTT to MySQL Logger
Listens MQTT topic and stores messages into MySQL.
"""

import json
import logging
import paho.mqtt.client as mqtt
import mysql.connector
from mysql.connector import pooling

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "chat/messages"
DB_CONFIG = {
    "host": "127.0.0.1",
    "user": "mqtt_user",
    "password": "",  # Oma salasana tähän
    "database": "mqtt_chat"
    "charset": "utf8mb4",
}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)
db_pool = pooling.MySQLConnectionPool(
    pool_name="mqtt_pool",
    pool_size=5,
    host="127.0.0.1",
    user="mqtt_user",
    password="Oma salasana tähän",
    database="mqtt_chat",
)

def save_message(nickname: str, message: str, client_id: str):
    conn = None
    cursor = None
    try:
        conn = db_pool.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO messages (nickname, message, client_id)
            VALUES (%s, %s, %s)
            """,
            (nickname, message, client_id)
        )
        
        conn.commit()
        logger.info(f"Saved: [{nickname}] {message[:50]}...")
        except mysql.connector.Error as err:
            logger.error(f"DB error: {err}")
            finally:
                if cursor:
                    cursor.close()
                    if conn:
                        conn.close()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logger.info("Connected to MQTT broker")
        client.subscribe(MQTT_TOPIC)
        logger.info(f"Subscribed: {MQTT_TOPIC}")
        else:
            logger.error(f"MQTT connection error, code: {rc}")

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode("utf-8")
        data = json.loads(payload)
        nickname = data.get("nickname", "Unknown")[:50]
        text = data.get("text", "")
        client_id = data.get("clientId", "")[:100]

        if text:
            save_message(nickname, text, client_id)
            except json.JSONDecodeError:
                logger.warning(f"Invalid JSON: {msg.payload}")
                except Exception as e:
                    logger.error(f"Unexpected error: {e}")

def main():
    logger.info("MQTT Logger starting...")
    
    # test DB connection
    try:
        conn = db_pool.get_connection()
        conn.close()
        logger.info("DB connection OK")
        except mysql.connector.Error as err:
            logger.error(f"No DB connection: {err}")
            return

    client = mqtt.Client(client_id="mqtt_logger")
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_forever()
    
if __name__ == "__main__":
main()