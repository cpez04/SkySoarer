import requests
import json
import geocoder 
import haversine as hs

#gets list of nearby airports (we need to parse database to only get name and distance from user)
params = {
  'api_key': 'c6f24eaf-a7e1-412b-8fdc-f0ca0194c440',
}
method = 'flights'
api_base = 'http://airlabs.co/api/v9/'
api_result = requests.get(api_base+method, params)
api_response = api_result.json()["response"]

latlng=geocoder.ip('me').latlng
latitude = latlng[0]
longitude = latlng[1]

keys2 = []
values2 = []
dict2 = {}

count = 5
for row in api_response:
    if count == 0:
        break
    print(row['flight_iata'])
    count=count-1
    
  