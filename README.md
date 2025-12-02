# MQTT Chat – Real-Time Chat with MQTT + WebSockets + MySQL + LEMP (CSC Pouta)
![MySQL](https://img.shields.io/badge/MySQL-4479A1.svg?style=for-the-badge&logo=mysql&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![Nginx](https://img.shields.io/badge/Nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)
![MariaDB](https://img.shields.io/badge/MariaDB-003545?style=for-the-badge&logo=mariadb&logoColor=white)
![Python](https://img.shields.io/badge/Python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

A browser-based real-time chat application built using:

- **Mosquitto MQTT broker (Docker container)**
- **WebSocket listener (port 9001)**
- **Flask API for chat history from MySQL/MariaDB**
- **mqtt_logger.py to store MQTT messages into database**
- **Nginx reverse proxy (`/chat`, `/mqtt`, `/api`)**
- **GitHub for code management**

---

## Project Structure
```
mqtt-chat/
│
├── api.py
├── docker-compose.yml
├── mqtt_logger.py
└── requirements.txt

web/
└──chat/
  │
  ├── index.html
  ├── script.js
  └── style.css
```
## Components

### Flask API (`api.py`)
- Provides: `/api/messages?limit=10`
- Fetches latest chat messages from the `mqtt_chat.messages` table
- Returns messages in order **oldest → newest**
- Used by frontend to reload the **last 10 messages on page refresh**

### MQTT Logger (`mqtt_logger.py`)
- Listens topic `chat/messages`
- Inserts new chat messages into MySQL database
- Logs database success/failure
- Enables realtime database message collection
- Runs as a **systemd service** (`mqtt-logger.service`)

## API service as a Systemd service

### `/etc/systemd/system/mqtt-api.service`

```ini
[Unit]
Description=MQTT Chat History API (Flask)
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/mqtt-chat
ExecStart=/home/ubuntu/mqtt-chat/venv/bin/python3 api.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```
Activation:
```bash
sudo systemctl daemon-reload
sudo systemctl enable mqtt-api
sudo systemctl start mqtt-api
sudo systemctl status mqtt-api
```
### Nginx Reverse Proxy
Routes configured in `/etc/nginx/sites-available/lemp`:
```nginx
location /chat {
    alias /var/www/lemp/chat;
    try_files $uri $uri/ /chat/index.html;
}

location /mqtt {
    proxy_pass http://127.0.0.1:9001;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
}

location /api {
    proxy_pass http://127.0.0.1:5000;
    proxy_http_version 1.1;
}
```
Reload Nginx:
```bash
sudo nginx -t
sudo systemctl reload nginx
```
## Installation & Setup
### Create Database + User
```sql
CREATE DATABASE IF NOT EXISTS mqtt_chat
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

DROP USER IF EXISTS 'mqtt_user'@'localhost';
DROP USER IF EXISTS 'mqtt_user'@'127.0.0.1';

CREATE USER 'mqtt_user'@'localhost' IDENTIFIED BY 'YourStrongPasswordHere';
CREATE USER 'mqtt_user'@'127.0.0.1' IDENTIFIED BY 'YourStrongPasswordHere';

GRANT ALL PRIVILEGES ON mqtt_chat.* TO 'mqtt_user'@'localhost';
GRANT ALL PRIVILEGES ON mqtt_chat.* TO 'mqtt_user'@'127.0.0.1';
FLUSH PRIVILEGES;
```
### Allow Flask API port access
API runs on: 5000 (bound to 0.0.0.0 so Nginx can access it)
### Start Flask API
```bash
cd /home/ubuntu/mqtt-chat
source venv/bin/activate
python3 api.py &
```
### Test API locally
```bash
curl http://127.0.0.1:5000/api/messages?limit=10
```
### Start MQTT Logger as service
```pgsql
sudo nano /etc/systemd/system/mqtt-logger.service
sudo systemctl daemon-reload
sudo systemctl enable mqtt-logger
sudo systemctl start mqtt-logger
sudo systemctl status mqtt-logger
```
---
## Testing the MQTT broker
Check WebSocket listener:
```bash
mosquitto_sub -h localhost -p 1883 -t "chat/messages"

mosquitto_pub -h localhost -p 1883 -t "chat/messages" \
  -m "{\"nickname\":\"Tester\",\"text\":\"Hello from terminal\",\"clientId\":\"cli-001\"}"
```
If messages appear, MQTT works.

---
# Technologies Used

| Component | Purpose |
|---|---|
| **Nginx** | Web server + reverse proxy for `/chat`, `/mqtt`, `/api` |
| **Mosquitto MQTT** | Message broker running inside Docker |
| **WebSockets** | MQTT WebSocket listener on port `9001`, proxied via `/mqtt` |
| **MariaDB** | MySQL-compatible database storing chat messages |
| **Flask (Python)** | REST API for chat history and timestamp formatting |
| **mqtt_logger.py (Python service)** | Listens `chat/messages` topic and inserts messages into DB |
| **JavaScript (mqtt.js client)** | Real-time messages received in browser + publish messages |
| **CSS** | Chat UI styling |
| **Systemd** | Keeps API and MQTT logger running 24/7 |
| **Docker Compose** | Runs the MQTT broker and config as containers |

![Docker](https://img.shields.io/badge/Docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)
![CSS](https://img.shields.io/badge/CSS-%23663399.svg?style=for-the-badge&logo=css&logoColor=white)

## Current Status
| Feature                             | Works? |
| ----------------------------------- | ------ |
| MQTT broker (Docker)                | ✔ Yes  |
| WebSockets (`/mqtt` via Nginx)      | ✔ Yes  |
| Flask API history (`/api/messages`) | ✔ Yes  |
| Last 10 messages on page reload     | ✔ Yes  |
| New messages stored into DB         | ✔ Yes  |
| Chat works                          | ✔ Yes  |
| Timestamps show                     | ✔ Yes  |
| Right timezone                      | ✔ Yes  |
