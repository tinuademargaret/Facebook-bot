import json
import requests

api_key = 'AIzaSyBCvwxLoAmIwGKBsOTtuQIJ4dpVuv2ALPk'


def get_attractions(place):
	search_term = 'attractions+in+'+ place
	url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?query=' + search_term + '&key=' + api_key + '&type=point_of_interest'
	r = requests.get(url)
	response = json.loads(r.text)
	result = ''
	locations = response['results']
	for location in locations:
		name = location['name']
		address = location['formatted_address']
		result += name + ', ' + address + '. '
	return result

if __name__ == '__main__':
	print(get_attractions('Ogbomosho'))