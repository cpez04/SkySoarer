import requests
import json

url = "https://skyscanner44.p.rapidapi.com/search"

querystring = {"adults":"2","origin":"EWR","destination":"KUL","departureDate":"2022-12-11","currency":"USD"}

headers = {
	"X-RapidAPI-Key": "49e1e79da8msh462c078111aa514p12ee18jsn10c23c73dcc6",
	"X-RapidAPI-Host": "skyscanner44.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)

#api_response = response.json()['itineraries']['buckets'][0]['items'][0]['legs'][0]['segments'][0]['operatingCarrier']['name']#gets name of operating airlines for 0th row
api_response = response.json()['itineraries']['buckets'][0]['items']

keys = []
values = []
dict = {}
length = len(api_response)

# create a list of names
for i in range(length):
    tmp = []
    keys.append(api_response[i]['legs'][0]['segments'][0]['operatingCarrier']['name']) 

    # insert formatted price, stop count, flight number in tmp
    tmp.append(api_response[i]['price']['formatted'])
    tmp.append(api_response[i]['legs'][0]['stopCount'])
    tmp.append(api_response[i]['legs'][0]['segments'][0]['flightNumber'])
    tmp.append(api_response[i]['legs'][0]['durationInMinutes'])

    # insert tmp into values
    values.append(tmp)

# pair key-value


print(keys)
print(values)