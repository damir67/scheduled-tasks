#import requests
import os
#from twilio.rest import Client
#from twilio.http.http_client import TwilioHttpClient
import requests
from twilio.rest import Client


account_sid = os.environ.get("ACCOUNT_SID")
auth_token = os.environ.get("AUTH_TOKEN")

api_key = os.environ.get("OWM_API_KEY")
OWM_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"


weather_params = {
    "lat": 45.815010, # ZG
    "lon": 15.981919,
    "appid": api_key,
    "cnt" : 4,
}

response = requests.get("https://api.openweathermap.org/data/2.5/forecast", params=weather_params)

response.raise_for_status()
#print (response.status_code)
waether_data = response.json()

#time_sec_start = waether_data["list"][0]["dt"]

#rain = False
will_rain = False

for hour_data in waether_data["list"]:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700 :
        will_rain = True

if will_rain:
    #print("Bring an umbrella")
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}

    client = Client(account_sid, auth_token, http_client=proxy_client)
    message = client.messages.create(
        body="It's going to rain today. Bring an ☂️",
        from_="+13603835195",
        to="+385912548567"
    )
    print(message.status)
