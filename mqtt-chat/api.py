#!/usr/bin/env python3

import pymysql
from flask import Flask, jsonify, request

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
        """
        SELECT
            id AS ID,
            nickname,
            message,
            client_id,
            created_at
        FROM messages
        ORDER BY created_at DESC
        LIMIT %s
        """,
        (limit,)
    )

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    # Formatoi timestampit kaikkiin viesteihin
    for r in rows:
        if r.get("created_at"):
            r["created_at"] = r["created_at"].strftime("%d.%m.%Y %H:%M:%S")

    # Käännä vanhimmat ensin → uusin alas
    return jsonify(list(reversed(rows)))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
