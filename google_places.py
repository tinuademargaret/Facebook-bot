import json
import requests

# api key - AIzaSyBCvwxLoAmIwGKBsOTtuQIJ4dpVuv2ALPk

def get_attractions(place):

	search_term = 'attractions+in+' + place

	r = requests.get('https://maps.googleapis.com/maps/api/place/textsearch/json?query=' + search_term + '&key=AIzaSyBCvwxLoAmIwGKBsOTtuQIJ4dpVuv2ALPk&type=point_of_interest')
	response = json.loads(r.text)
	result = []
	locations = response['result']
	for location in locations:
		name = location['name']
		address = location['formatted_address']
		result.append(name + ', ' + address)
	return result

