import requests
import json

flight_icao, flight_iata = 0

# when user determines a specific flight, returns an info report (maybe here allows save as pdf)
params = {
  'api_key': 'c6f24eaf-a7e1-412b-8fdc-f0ca0194c440',
  'flight_icao': flight_icao,
  'flight_iata': flight_iata
}

method = 'flight'
api_base = 'http://airlabs.co/api/v9/'
api_result = requests.get(api_base+method, params)

list = [] # allows us to change easily which data is shown to user
for item in list:
  print(item + ": " + api_result.json()["response"]["airports"][2]['name']) # need to see data structure --> Chris