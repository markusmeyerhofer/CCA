import os
import time
import requests
from datetime import datetime

try:
    os.mkdir("CAINS")
except OSError as error:
    True

while True:

    url = "https://api.nomics.com/v1/currencies/ticker?key=7447a1d2a3e1e93b18d9bbf0006ed748"
    request = requests.get(url)
    data = request.json()

    for i in data:

        day = datetime.now().strftime("%d-%m-%Y")
        hours = datetime.now().strftime("%H:%M")

        try:
            buildstream = "" + i["id"] + ";" + i["name"] + ";" + i["price"] + ";" + i[
                "num_exchanges"] + ";" + i["market_cap"] + ";" + i["1d"]["price_change_pct"] + ";" + \
                          i["high"] + ";" + i["1d"]["volume_change_pct"] + ";" \
                          + i["1d"]["market_cap_change_pct"] + ";" + hours + ";" + day + "\n"

            a = open("CAINS\\cains_" + day + ".csv", "a+")
            a.write(buildstream)
            print(buildstream)
            del buildstream
            del day
            del hours
            a.close()

        except KeyError:
            False

    request.close()
    print("===============================================")

    time.sleep(60)