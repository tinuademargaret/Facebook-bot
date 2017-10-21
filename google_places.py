import json
import requests

api_key = 'AIzaSyBCvwxLoAmIwGKBsOTtuQIJ4dpVuv2ALPk'
place = 'Abuja'
search_term = 'attractions+in+'+ place
url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?query=' + search_term + '&key=' + api_key + '&type=point_of_interest'
r = requests.get(url)
response = json.loads(r.text)
result = []
locations = response['results']
for location in locations:
	name = location['name']
	address = location['formatted_address']
	result.append((name, address))
for item in result:
	print(item)

