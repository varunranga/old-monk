import requests
import json

send_url = 'http://freegeoip.net/json'
r = requests.get(send_url)
j = json.loads(r.text)
lat = j['latitude']
lon = j['longitude']

print("Latitude :",lat)
print("Longitude :",lon)

s=repr(lat)+","+repr(lon);

from geopy.geocoders import Nominatim
geolocator = Nominatim()

print(s)

location = geolocator.reverse(s)
print(location.address)
#print(location.raw)