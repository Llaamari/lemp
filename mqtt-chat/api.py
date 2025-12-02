#!/usr/bin/env python3
import pymysql
from flask import Flask, jsonify, request
from datetime import timedelta

app = Flask(__name__)

@app.route("/api/messages", methods=["GET"])
def get_messages():
    limit = request.args.get("limit", 10, type=int)

    conn = pymysql.connect(
        host="127.0.0.1",
        user="mqtt_user",
        password="",  # Oma salasana tähän
        database="mqtt_chat",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
    )

    cursor = conn.cursor()
    cursor.execute(
        "SELECT id AS ID, nickname, message, client_id, created_at "
        "FROM messages "
        "ORDER BY created_at DESC "
        "LIMIT %s", (limit,)
    )

    rows = cursor.fetchall()
    conn.close()

    # Aikaformaatti
    for r in rows:
        if "created_at" in r and r["created_at"]:
            r["created_at"] = (r["created_at"] + timedelta(hours=2)).strftime("%d.%m.%Y %H:%M:%S")

    return jsonify(rows[::-1])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)  # jää päälle ja kuuntelemaan