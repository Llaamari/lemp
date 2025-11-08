<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <title>LEMP Stack Test</title>
        <link rel="stylesheet" type="text/css" href="style.css">
    </head>
    
    <body>
        <h1>Tervetuloa LEMP-sivulle!</h1>
        <p>Palvelimen kellonaika SQL-tietokannasta:</p>
        
        <section class="clock-container">
            <h2>Palvelimen kellonaika SQL-tietokannasta</h2>
            <div id="clock">
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
        </section>
        
        <script src="script.js"></script>
    </body>
</html>
