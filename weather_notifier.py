# -*- coding: UTF-8 -*-
import requests
import datetime
import json
from twilio.rest import TwilioRestClient
from pprint import pprint

uri = 'http://api.openweathermap.org/data/2.5/weather'
zipcode = '06770'
units = 'imperial'

r = requests.get(uri, params={'zip': zipcode, 'units': units})

if r.status_code == 200:
    raw_json = r.text
    data = json.loads(raw_json)

    sunrise = data['sys']['sunrise']
    sunset = data['sys']['sunset']

    # convert unix timestamp to readable format
    sunrise = datetime.datetime.fromtimestamp(sunrise).strftime('%H:%MAM')
    sunset = datetime.datetime.fromtimestamp(sunset).strftime('%H:%MPM')

    current_temp = data['main']['temp']
    low_temp = data['main']['temp_min']
    high_temp = data['main']['temp_max']

    # convert the temps to more readable format
    # this will round the decimal down and add the units at the end
    current_temp = str(int(current_temp)) + '°F'
    low_temp = str(int(low_temp)) + '°F'
    high_temp = str(int(high_temp)) + '°F'

    humidity = data['main']['humidity']
    humidity = str(humidity) + '%'

    description = data['weather'][0]['description']

else:
    raw_json = r.text
    data = json.loads(raw_json)
    pprint(data)

credentials = json.load(open('credentials.json', 'r'))
account_sid = credentials['account-sid']
auth_token = credentials['auth-token']
twilio_number = credentials['twilio-number']
my_number = credentials['my-number']

weather_data = {
        'sunrise': sunrise,
        'sunset': sunset,
        'current_temp': current_temp,
        'low_temp': low_temp,
        'high_temp': high_temp,
        'humidity': humidity,
        'description': description
        }

message = (
        "You're weather forecast for the day:\n"
        "{description} with a low of {low_temp} and a high of {high_temp}. "
        "The current temperature is {current_temp} with a humidity of"
        "{humidity}.\n\n"
        "Sunrise: {sunrise}\nSunset: {sunset}"
        ).format(**weather_data)

client = TwilioRestClient(account_sid, auth_token)
message = client.messages.create(to=my_number, from_=twilio_number, body=message)
