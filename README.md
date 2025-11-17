# LEMP Stack Project (cPouta)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black) ![Nginx](https://img.shields.io/badge/Nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white) ![MariaDB](https://img.shields.io/badge/MariaDB-003545?style=for-the-badge&logo=mariadb&logoColor=white) ![PHP](https://img.shields.io/badge/PHP-%23777BB4.svg?style=for-the-badge&logo=php&logoColor=white)

This repository contains a LEMP stack (Linux, Nginx, MariaDB, PHP) assignment running on CSC's cPouta cloud service.  
The webpage displays the current server time fetched from the SQL database and updates it in real time on the client side.

---

## Installation Steps

### 1. Virtual Machine
- Create a new virtual machine in CSC’s cPouta service, on a different port than Apache.
- Make sure **HTTP port (80)** is open to the public, so the people can access the page.

### 2. Install the LEMP Stack
![Bash Script](https://img.shields.io/badge/Bash_Script-%23121011.svg?style=for-the-badge&logo=gnu-bash&logoColor=white)
```bash
sudo apt update
sudo apt install nginx mariadb-server php-fpm php-mysql -y
```
### 3. Start and Enable Services
![Bash Script](https://img.shields.io/badge/Bash_Script-%23121011.svg?style=for-the-badge&logo=gnu-bash&logoColor=white)
```bash
sudo systemctl enable nginx
sudo systemctl start nginx
sudo systemctl enable mariadb
sudo systemctl start mariadb
sudo systemctl enable php8.3-fpm
sudo systemctl start php8.3-fpm
```
### 4. Place the Web Files
Path:
```bash
/var/www/lemp/html/
├── index.php
├── style.css
└── script.js
```
### 5. Access the Page in Your Browser
```cpp
http://<server_IP>
```
## Functionality
- The main page (`index.php`) fetches the current time from the SQL database using `SELECT NOW()`.
- JavaScript updates the displayed time dynamically in real time.
- The time format follows style:<br>
dd.mm.yyyy, hh:mm:ss
- The page has been slightly customized with colors and text for a personal touch.
## Technologies Used
| Component           | Description                                    |
| ------------------- | ---------------------------------------------- |
| **Nginx**           | Web server (serving PHP via FastCGI)           |
| **MariaDB**         | Database used to retrieve the server time      |
| **PHP-FPM**         | Executes the PHP code in `index.php`           |
| **HTML + CSS + JS** | Page structure, styling, and real-time updates |

![PHP](https://img.shields.io/badge/PHP-%23777BB4.svg?style=for-the-badge&logo=php&logoColor=white) ![CSS3](https://img.shields.io/badge/CSS3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white) ![JavaScript](https://img.shields.io/badge/JavaScript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)
## Project URL
[Live site](http://86.50.22.232/)
