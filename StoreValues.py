import mariadb
import sys

#ssh -L 3306:localhost:3306 pi@cca1.hopto.org

# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user="phpmyadmin",
        password="F1xKCrC7ydVr",
        host="localhost",
        port=3306,
        database="CCA"
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()
print("ES FUNKTIONIERT!!!!")
cur.close()

if(0):
    url = "https://api.nomics.com/v1/currencies/ticker?key=7447a1d2a3e1e93b18d9bbf0006ed748"
    request = requests.get(url)
    data = request.json()

    for i in data:
        print(i["price"])

    request.close()
    print("===============================================")
