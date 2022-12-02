import requests
import json

flight_icao = 'AAL6'
flight_iata = 'AA6'

# when user determines a specific flight, returns an info report (maybe here allows save as pdf)
params = {
  'api_key': 'c6f24eaf-a7e1-412b-8fdc-f0ca0194c440',
  'flight_icao': flight_icao,
  'flight_iata': flight_iata
}

method = 'flight'
api_base = 'http://airlabs.co/api/v9/'
api_result = requests.get(api_base+method, params)
api_response = api_result.json()['response']

key = ['aircraft_icao', 'airline_iata']
value = []
for items in key:
  value.append(api_response[items])

print(value)
# need to see data structure --> Chris