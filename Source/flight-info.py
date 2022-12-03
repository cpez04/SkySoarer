import requests
import json



# when user determines a specific flight, returns an info report (maybe here allows save as pdf)
params = {
        'api_key': 'c6f24eaf-a7e1-412b-8fdc-f0ca0194c440',
        'flight_iata': 'AA6',
        }

try:
  method = 'flight'
  api_base = 'http://airlabs.co/api/v9/'
  api_result = requests.get(api_base+method, params)
  api_response = api_result.json()['response']
except:
  print("unsuccesff")
  
key = ['dep_name', 'arr_name', 'status', 'dep_time', 'dep_gate', 'arr_gate'] 
value = []
dict = {}

for items in key:
  try:
    value.append(api_response[items])
  except:
    value.append("Not Available")

for i in range(len(key)):
  dict[key[i]] = value[i]
  
print(dict)


  
# need to see data structure --> Chris