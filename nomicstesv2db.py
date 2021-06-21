import os
import time
import requests
import gc
from datetime import datetime

import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    username="root",
    password="",
    database="krypto"
)

curs = mydb.cursor()

while True:

    url = "https://api.nomics.com/v1/currencies/ticker?key=7447a1d2a3e1e93b18d9bbf0006ed748"
    request = requests.get(url)
    data = request.json()

    for i in data:

        day = datetime.now().strftime("%d.%m.%Y-%H.%M.%S")

        try:

            print("...")
            curs.execute("INSERT INTO t_currency(short,price,datum) values ('" + str(i["id"]) + "'," + str(
                i["price"]) + ",'" + str(day) + "')")
            mydb.commit()

        except KeyError:
            False

    request.close()
    print("===============================================")

    time.sleep(60)