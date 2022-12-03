import requests
import json



# when user determines a specific flight, returns an info report (maybe here allows save as pdf)
params = {
        'api_key': 'c6f24eaf-a7e1-412b-8fdc-f0ca0194c440',
        'flight_iata': 'AA198',
        }

try:
  method = 'flights'
  api_base = 'http://airlabs.co/api/v9/'
  api_result = requests.get(api_base+method, params)
  api_response = api_result.json()['response']
except:
  print("unsuccesff")

print(api_response)
  

  
# need to see data structure --> Chris