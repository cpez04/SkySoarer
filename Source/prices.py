import requests

url = "https://skyscanner44.p.rapidapi.com/search"

querystring = {"adults":"1","origin":"EWR","destination":"MIA","departureDate":"2022-12-11","currency":"USD"}

headers = {
	"X-RapidAPI-Key": "49e1e79da8msh462c078111aa514p12ee18jsn10c23c73dcc6",
	"X-RapidAPI-Host": "skyscanner44.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)