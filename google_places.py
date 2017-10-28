import json
import requests

# api key - AIzaSyBCvwxLoAmIwGKBsOTtuQIJ4dpVuv2ALPk

search_term = 'attractions+in+Lagos'

r = requests.get('https://maps.googleapis.com/maps/api/place/textsearch/json?query=' + search_term + '&key=AIzaSyBCvwxLoAmIwGKBsOTtuQIJ4dpVuv2ALPk&type=point_of_interest')
response = json.loads(r.text)
result = []
locations = response['result']
for location in locations:
	name = location['name']
	address = location['formatted_address']
	result.append((name, address))
for item in result:
	print(item)

