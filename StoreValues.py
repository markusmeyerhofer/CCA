import mariadb
import sys
import requests
from datetime import datetime

# ssh -L 3306:localhost:3306 pi@cca1.hopto.org

day = datetime.now().strftime("%Y-%m-%d")
hours = datetime.now().strftime("%H:%M:%S")

url = "https://api.nomics.com/v1/currencies/ticker?key=7447a1d2a3e1e93b18d9bbf0006ed748"
request = requests.get(url)
data = request.json()
request.close()

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
cur.execute("SELECT price, circulating_supply, market_cap, num_exchanges, volume FROM CRYPTO_DATA WHERE timestamp > "
            "now() - interval 15 minute ORDER BY timestamp ASC LIMIT 1;")
rows = cur.fetchone()

price_past, circulating_supply_past, market_cap_past, num_exchanges, volume_past = rows

# Calculating changes
price_change_rel = str(price_past/float(data[0]["price"])*100)
circulating_supply_change_rel = str(circulating_supply_past/int(data[0]["circulating_supply"])*100)
market_cap_change_rel = str(market_cap_past/int(data[0]["market_cap"])*100)
num_exchanges_change_rel = str(num_exchanges/int(data[0]["num_exchanges"])*100)
volume_change_rel = str(volume_past/float(data[0]["1d"]["volume"])*100)

cur.execute("INSERT INTO CRYPTO_DATA(id,name,price,circulating_supply,market_cap,num_exchanges,num_pairs,volume,"
            "price_change_rel,circulating_supply_change_rel,market_cap_change_rel,num_exchanges_change_rel,"
            "volume_change_rel,timestamp) values('" + data[0]["id"] + "','" + data[0]["name"] + "'," + data[0]["price"]
            + "," + data[0]["circulating_supply"] + "," + data[0]["market_cap"] + "," + data[0]["num_exchanges"]
            + "," + data[0]["num_pairs"] + "," + data[0]["1d"]["volume"] + "," + price_change_rel + "," +
            circulating_supply_change_rel + "," + market_cap_change_rel + "," + num_exchanges_change_rel +
            "," + volume_change_rel + ",CURRENT_TIMESTAMP)")

# cur.execute("SELECT * FROM CRYPTO_DATA")
conn.commit()

cur.close()

# price_change_rel = price - price 3min before



