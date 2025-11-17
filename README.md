# Full LEMP + Streamlit Project (cPouta)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![Nginx](https://img.shields.io/badge/Nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)
![MariaDB](https://img.shields.io/badge/MariaDB-003545?style=for-the-badge&logo=mariadb&logoColor=white)
![PHP](https://img.shields.io/badge/PHP-%23777BB4.svg?style=for-the-badge&logo=php&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-%23FE4B4B.svg?style=for-the-badge&logo=streamlit&logoColor=white)

This repository contains a full LEMP stack + Streamlit application deployed on CSC’s cPouta cloud service.  
The project includes:

- A PHP-based public homepage served via Nginx  
- Real-time clock fetched from the MariaDB SQL database  
- A Streamlit data-analysis application running as a system service  
- Nginx reverse proxy routing the Streamlit app to:  
  **http:/<server-ip>/data-analysis**  
- A link to the Streamlit app on the homepage  
- GitHub used for full version control

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
```
---

# LEMP Stack Setup

## 1. Install Packages
![Bash Script](https://img.shields.io/badge/Bash_Script-%23121011.svg?style=for-the-badge&logo=gnu-bash&logoColor=white)
```bash
sudo apt update
sudo apt install nginx mariadb-server php php-fpm php-mysql -y
```
## 2. Enable and Start Services
![Bash Script](https://img.shields.io/badge/Bash_Script-%23121011.svg?style=for-the-badge&logo=gnu-bash&logoColor=white)
```bash
sudo systemctl enable nginx --now
sudo systemctl enable mariadb --now
sudo systemctl enable php8.3-fpm --now
```
# Homepage (PHP)
The homepage is served from:
```
/var/www/lemp/web/
```
It includes:
- Personalized styling
- JavaScript-based real-time UI updates
- PHP query retrieving SQL server time:<br>
  ![MySQL](https://img.shields.io/badge/MySQL-4479A1.svg?style=for-the-badge&logo=mysql&logoColor=white)
  ```sql
  SELECT NOW();
  ```
The clock is displayed in time format:<br>
dd.mm.yyyy, hh:mm:ss

Access the homepage:
```cpp
http://<server-ip>
```
# Streamlit Application
The Streamlit app reads real data from a MySQL/MariaDB database using `pymysql`.
## 1. Virtual Environment
![Bash Script](https://img.shields.io/badge/Bash_Script-%23121011.svg?style=for-the-badge&logo=gnu-bash&logoColor=white)
```bash
cd /var/www/lemp/streamlit_app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
## 2. requirements.txt
![PowerShell](https://img.shields.io/badge/PowerShell-%235391FE.svg?style=for-the-badge&logo=powershell&logoColor=white)
```shell
streamlit>=1.30
pymysql>=1.1
pandas>=2.0
```
## 3. Run Streamlit as a System Service
`/etc/systemd/system/streamlit.service`
```ini
[Unit]
Description=Streamlit Service
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/var/www/lemp/streamlit_app
ExecStart=/var/www/lemp/streamlit_app/venv/bin/python -m streamlit run app.py --server.port 8501 --server.address 0.0.0.0
Restart=always

[Install]
WantedBy=multi-user.target
```
Enable and start:<br>
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
# Nginx Reverse Proxy for Streamlit
The `/data-analysis` route is forwarded to port 8501:<br>
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
Restart Nginx:<br>
![Bash Script](https://img.shields.io/badge/Bash_Script-%23121011.svg?style=for-the-badge&logo=gnu-bash&logoColor=white)
```bash
sudo systemctl restart nginx
```
Access Streamlit through Nginx:
```cpp
http://<server-ip>/data-analysis
```
# Link on Homepage
The homepage includes a link that directs users to the Streamlit data-analysis page:<br>
![PHP](https://img.shields.io/badge/PHP-%23777BB4.svg?style=for-the-badge&logo=php&logoColor=white)
```php-template
<a href="/data-analysis">Go to Data Analysis App</a>
```
# Database
The system uses a MariaDB database for both:
- Retrieving real server time in `index.php`
- Displaying data inside the Streamlit app (via pymysql)

Example Python connection:<br>
![Python](https://img.shields.io/badge/Python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
```python
conn = pymysql.connect(
    host="localhost",
    user="appuser",
    password="your_password",
    database="your_database",
    charset="utf8mb4"
)
```
# Technologies Used
| Component       | Purpose                       |
| --------------- | ----------------------------- |
| **Nginx**       | Web server + reverse proxy    |
| **PHP-FPM**     | Runs the PHP homepage         |
| **MariaDB**     | Stores data + server time     |
| **Streamlit**   | Data-analysis web application |
| **Python**      | Logic in Streamlit app        |
| **HTML/CSS/JS** | Frontend customization        |
| **Systemd**     | Runs Streamlit as a service   |
| **GitHub**      | Version control               |

![Python](https://img.shields.io/badge/Python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![HTML5](https://img.shields.io/badge/Html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![CSS](https://img.shields.io/badge/CSS-%23663399.svg?style=for-the-badge&logo=css&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)
![GitHub](https://img.shields.io/badge/GitHub-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)
# Live URLs
- [Homepage](http://86.50.22.232/)
- [Streamlit App](http://86.50.22.232/data-analysis/)
