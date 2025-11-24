# Cron + API + MySQL + Streamlit + LEMP (cPouta)
![MySQL](https://img.shields.io/badge/MySQL-4479A1.svg?style=for-the-badge&logo=mysql&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-%23FE4B4B.svg?style=for-the-badge&logo=streamlit&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![Nginx](https://img.shields.io/badge/Nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)
![MariaDB](https://img.shields.io/badge/MariaDB-003545?style=for-the-badge&logo=mariadb&logoColor=white)
![PHP](https://img.shields.io/badge/PHP-%23777BB4.svg?style=for-the-badge&logo=php&logoColor=white)

This project extends the previous LEMP + Streamlit setup by adding:

✔ Automated API data collection using **cron**  
✔ Weather data fetching from **OpenWeatherMap API** (every 15 minutes)  
✔ Currency exchange rate data from **Frankfurter API**  
✔ Automatic data storage into **MySQL / MariaDB**  
✔ A multi-tab Streamlit dashboard for data visualization  
✔ Reverse proxy configuration via Nginx for `/data-analysis`  
✔ All code managed via GitHub (API keys excluded)

The live application is running on CSC’s cPouta VPS.

---

# Project Structure
```
/var/www/lemp/
│
├── web/
│ ├── index.php
│ ├── style.css
│ └── script.js
│
└── streamlit_app/
├── app.py
├── requirements.txt
└── venv/

/home/ubuntu/cron_assignment/
│── fetch_weather.py
│── fetch_exchange.py
│── fetch_weather.sh
│── requirements.txt
│── weather_cron.log
└── exchange_cron.log
```
---

# Homepage (PHP)
The front page is served by Nginx and includes:

- A personalized layout  
- JavaScript-based real-time clock  
- Server time fetched via MariaDB  
- A link to the Streamlit app under `/data-analysis`  
- No personal information shown (for anonymous peer review)

Homepage URL:<br>
[http://86.50.22.232/](http://86.50.22.232/)

---

# Streamlit Application

The Streamlit dashboard includes **three fully interactive tabs**:

### Weather (Oulu)
- Data fetched every 15 minutes via cron  
- Stored in **weather_db.weather_data**  
- Displays:
  - City  
  - Temperature  
  - Description  
  - Timestamp (DD.MM.YYYY HH:MM:SS)

### Exchange Rates
- Exchange data pulled from Frankfurter API (`EUR → USD/GBP/JPY/SEK`)
- Stored in **finance_db.exchange_rates**
- Interactive Altair line chart with:
  - Currency selector  
  - Hover tooltips  
  - Automatic time sorting  

### Temperature Measurements
- Local test data stored in **testdb.temperature_data**
- Two sub-tabs:
  - Latest measurements  
  - Line chart trend  

App URL (via Nginx reverse proxy):<br>
[http://86.50.22.232/data-analysis/](http://86.50.22.232/data-analysis/)

---

# Streamlit System Service

`/etc/systemd/system/streamlit.service`
```ini
[Unit]
Description=Streamlit Service
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/var/www/streamlit_app
ExecStart=/var/www/streamlit_app/venv/bin/python -m streamlit run app.py --server.port 8501 --server.address 0.0.0.0
Restart=always

[Install]
WantedBy=multi-user.target
```
Activate:<br>
![Bash Script](https://img.shields.io/badge/Bash_Script-%23121011.svg?style=for-the-badge&logo=gnu-bash&logoColor=white)
```bash
sudo systemctl daemon-reload
sudo systemctl enable streamlit
sudo systemctl start streamlit
```
Test locally:
```cpp
http://<server-ip>:8501
```
# Automated Data Fetching (Cron)
The cron job runs every 15 minutes:<br>
```ruby
*/15 * * * * /bin/bash /home/ubuntu/cron_assignment/fetch_weather.sh
```
`fetch_weather.sh`
- Includes API key as environment variable
- Creates and activates a virtual environment
- Installs Python dependencies
- Runs both data-fetch scripts
- Stores logs (`weather_cron.log`, `exchange_cron.log`)

Weather API
- Source: OpenWeatherMap
- API key stored securely (NOT in GitHub)

Currency API
- Source: Frankfurter API (no key required)
# Nginx Reverse Proxy
`/etc/nginx/sites-available/default` includes:<br>
![Nginx](https://img.shields.io/badge/Nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)
```nginx
location /data-analysis/ {
    proxy_pass http://localhost:8501/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```
Reload:<br>
![Bash Script](https://img.shields.io/badge/Bash_Script-%23121011.svg?style=for-the-badge&logo=gnu-bash&logoColor=white)
```bash
sudo nginx -t
sudo systemctl reload nginx
```
# MySQL Databases
Weather Data Table (`weather_db`)<br>
![MySQL](https://img.shields.io/badge/SQL-4479A1.svg?style=for-the-badge&logo=mysql&logoColor=white)
```sql
CREATE TABLE IF NOT EXISTS weather_data (
  id INT AUTO_INCREMENT PRIMARY KEY,
  city VARCHAR(50),
  temperature FLOAT,
  description VARCHAR(100),
  timestamp DATETIME
);
```
Currency Table (`finance_db`)<br>
![MySQL](https://img.shields.io/badge/SQL-4479A1.svg?style=for-the-badge&logo=mysql&logoColor=white)
```sql
CREATE TABLE IF NOT EXISTS exchange_rates (
  id INT AUTO_INCREMENT PRIMARY KEY,
  base VARCHAR(10),
  currency VARCHAR(10),
  rate FLOAT,
  timestamp DATETIME
);
```
# Technologies Used
| Component     | Purpose                          |
| ------------- | -------------------------------- |
| **Nginx**     | Web server + reverse proxy       |
| **PHP-FPM**   | Serves homepage                  |
| **MariaDB**   | All SQL databases                |
| **Python**    | Streamlit + API fetching scripts |
| **Streamlit** | Interactive data dashboard       |
| **cron**      | Automated 15min API data pulling |
| **Systemd**   | Keeps Streamlit alive 24/7       |
| **GitHub**    | Version control                  |

![CSS](https://img.shields.io/badge/CSS-%23663399.svg?style=for-the-badge&logo=css&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)
![Python](https://img.shields.io/badge/Python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![GitHub](https://img.shields.io/badge/GitHub-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)

# Live URLs
- [Homepage](http://86.50.22.232/)
- [Streamlit Data Analysis App](http://86.50.22.232/data-analysis/)
