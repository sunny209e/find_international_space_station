import requests , smtplib, time
from datetime import datetime

#variables and constants.
MY_LAT = 26.912434
MY_LONG = 75.787270
email= "python209e@gmail.com"
password= "dxwrqbddbmjmlhmp"

def check_location():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_lats = float(data["iss_position"]["latitude"])
    iss_longs = float(data["iss_position"]["longitude"])

    if MY_LONG+5>=iss_longs>=MY_LONG-5 and MY_LAT+5>=iss_lats>=MY_LAT-5:
        return True
    return False

def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }
    response_2 = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response_2.raise_for_status()
    data_2 = response_2.json()
    sunrise = int(data_2["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data_2["results"]["sunset"].split("T")[1].split(":")[0])

    #storing the current hour
    time_now = datetime.now()
    current_hour= time_now.hour
    if sunrise>current_hour>sunset:
        return True
    return False

#main logic and email sending mechanism
while True:
    time.sleep(60)
    if check_location() and is_night():
        with smtplib.SMTP("smtp.gmail.com",587) as connection:
            connection.starttls()
            connection.login(user=email,password=password)
            connection.sendmail(from_addr=email,
                                to_addrs="sunnybishnoizod@gmail.com",
                                msg="Subject:Look up!\n\n"
                                    "ISS is currently above in the sky on your coordinates.")
