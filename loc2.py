import urllib3
import json

# Automatically geolocate the connecting IP
f = urllib3.urlopen('http://freegeoip.net/json/')
json_string = f.read()
f.close()
location = json.loads(json_string)
print(location)
location_city = location['city']
location_state = location['region_name']
location_country = location['country_name']
location_zip = location['zipcode']