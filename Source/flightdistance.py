import requests
import json
import geocoder 
import haversine as hs

from haversine import Unit

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
usertuple = (latitude,longitude)  

keys2 = []
values2 = []
dict2 = {}

for row in api_response:
  planetuple = (row['lat'], row['lng'])
  distance = hs.haversine(usertuple, planetuple, unit=Unit.MILES)
  
  if distance < 10:
    try:
      keys2.append(row['flight_iata'])
    except:
      keys2.append("None")
      
    values2.append(distance)

for i in range(len(keys2)):
  dict2[keys2[i]] = values2[i]
  
print(dict2)
    
  
  