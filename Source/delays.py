import requests
import json
#gets list of nearby airports (we need to parse database to only get name and distance from user)
params = {
  'api_key': 'c6f24eaf-a7e1-412b-8fdc-f0ca0194c440',
  'delay': '30',
  'type': 'departures',
  'dep_iata': 'EWR'
}
method = 'delays'
api_base = 'http://airlabs.co/api/v9/'
api_result = requests.get(api_base+method, params)
api_response = api_result.json()["response"]

count = 5
for row in api_response:
    if count == 0:
        break
    print(row['flight_iata'])
    count=count-1
    
  