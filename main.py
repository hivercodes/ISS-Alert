import requests
from datetime import datetime
import smtplib
import time


while True:
    time.sleep(60)
    MY_EMAIL = "lars@groundwave.se"
    PW = ""
    APPS = "apps@groundwave.se"


    MY_LAT = 59.2747287
    MY_LONG = 15.2151181
    response = requests.get(url="http://api.open-notify.org/iss-now.json")

    position = response.json()["iss_position"]

    long = position["longitude"]
    lat = position["latitude"]


    iss_position = (lat, long)
    my_position = (MY_LAT, MY_LONG)


    peramiters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    sunset_get = requests.get("https://api.sunrise-sunset.org/json", params=peramiters)
    sunset_get.raise_for_status()
    sunset_data = sunset_get.json()

    sunrise = int(sunset_data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(sunset_data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now()
    hour = int(time_now.hour)

    night = True

    if hour == sunset:
        night = True
    elif hour == sunrise:
        night = False


    iss_round_lat = int(iss_position[0].split(".")[0])
    iss_round_lng = int(iss_position[1].split(".")[0])


    if night == True:
        if iss_round_lat in range(round(my_position[0]) - 6, round(my_position[0]) + 6):
            if iss_round_lng in range(round(my_position[1]) - 6, round(my_position[1]) + 6):
                with smtplib.SMTP(host="mail.groundwave.se", port=587) as connection:
                    connection.starttls()
                    connection.login(user=APPS, password=PW)
                    connection.sendmail(from_addr=APPS,
                                        to_addrs=MY_EMAIL,
                                        msg=f"Subject:ISS spotted!\n\nISS is above at coordinates:\nlng:{iss_position[1]}\nlat:{iss_position[0]}")
