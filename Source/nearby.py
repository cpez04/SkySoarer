import requests
import json
#gets list of nearby airports (we need to parse database to only get name and distance from user)
params = {
  'api_key': 'c6f24eaf-a7e1-412b-8fdc-f0ca0194c440',
  'lat': '42.378021',
  'lng': '-71.116392',
  'distance': '30'
}
method = 'nearby'
api_base = 'http://airlabs.co/api/v9/'
api_result = requests.get(api_base+method, params)
api_response = api_result.json()["response"]["airports"] #prints informaiton for airports nearby

keys = []
values = []
length = len(api_response)
dicts = {}

for row in api_response:
  keys.append(row['name'])
  values.append(row['distance'])

for i in range (length):
  dicts[keys[i]] = values[i]
  
# print(len(api_response)) # prints # of nearby airports in given radius 

