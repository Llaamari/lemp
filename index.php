<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>LEMP Stack Test</title>
    <style>
        body {
            font-family: sans-serif;
            background-color: #eef;
            text-align: center;
            padding-top: 50px;
        }
        h1 { color: #0077cc; }
        .time {
            font-size: 1.5em;
            color: #222;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <h1>Tervetuloa LEMP-sivulle!</h1>
    <p>Tämä sivu pyörii Nginx + PHP + MariaDB -ympäristössä.</p>
    <p>Palvelimen kellonaika SQL-tietokannasta:</p>

    <div class="time" id="clock">
        <?php
            $conn = new mysqli("localhost", "root", "", "");
            if ($conn->connect_error) {
                die("Tietokantayhteys epäonnistui: " . $conn->connect_error);
            }
            $result = $conn->query("SELECT NOW() AS aika");
            if ($result && $row = $result->fetch_assoc()) {
                echo $row['aika'];
            } else {
                echo "Ajan hakeminen epäonnistui.";
            }
            $conn->close();
        ?>
    </div>

    <script>
        // Hae PHP:ltä saatu aika ja käynnistä JavaScript-kello
        const timeElem = document.getElementById("clock");
        const startTime = new Date(timeElem.textContent.trim());
        
        function updateClock() {
            const now = new Date(startTime.getTime() + (Date.now() - pageLoadTime));
            const yyyy = now.getFullYear();
            const mm = String(now.getMonth() + 1).padStart(2, '0');
            const dd = String(now.getDate()).padStart(2, '0');
            const hh = String(now.getHours()).padStart(2, '0');
            const mi = String(now.getMinutes()).padStart(2, '0');
            const ss = String(now.getSeconds()).padStart(2, '0');
            timeElem.textContent = `${yyyy}-${mm}-${dd} ${hh}:${mi}:${ss}`;
        }

        const pageLoadTime = Date.now();
        setInterval(updateClock, 1000);
    </script>
</body>
</html>
