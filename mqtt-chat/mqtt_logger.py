#!/usr/bin/env python3
import json
import logging
import pymysql
import paho.mqtt.client as mqtt
from mysql.connector import pooling

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "chat/messages"

DB_NAME = "mqtt_chat"

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

db_pool = pooling.MySQLConnectionPool(
    pool_name="mqtt_pool",
    pool_size=5,
    host="127.0.0.1",
    user="mqtt_user",
    password="", # Oma salasana tähän
    database=DB_NAME,
)

def save_message(nickname: str, message: str, client_id: str):
    try:
        conn = db_pool.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "INSERT INTO messages (nickname, message, client_id) VALUES (%s, %s, %s)",
            (nickname, message, client_id),
        )
        conn.commit()
        logger.info(f"Tallennettu: [{nickname}] {message[:40]}")

    except Exception as e:
        logger.error(f"INSERT ERROR: {e}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logger.info("MQTT connected ✔")
        client.subscribe(MQTT_TOPIC, qos=0)
    else:
        logger.error(f"MQTT failed: {rc}")

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode("utf-8"))
        nickname = data.get("nickname", "Tuntematon")[:50]
        text = data.get("text", "")
        client_id = data.get("clientId", "")[:100]

        if text:
            save_message(nickname, text, client_id)

    except Exception as e:
        logger.error(f"MQTT parse error: {e}")

def main():
    logger.info("MQTT logger käynnistyy…")
    client = mqtt.Client(
        client_id="mqtt_logger",
        clean_session=True,
        protocol=mqtt.MQTTv311,
    )
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_message = on_message

    # Connect and stay listening
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_forever()

if __name__ == "__main__":
    main()
