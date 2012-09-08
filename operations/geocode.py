from elixir import *
import requests, json
from urllib import urlencode
from models.local import Location
from time import sleep

class Geocoder(object):
    _geocode_url = 'http://maps.googleapis.com/maps/api/geocode/json'

    # use geocoding service to obtain lat/lon from address
    def geocode(self, location):
        address = location.address
        if None != address:
            address = address.encode('ascii', 'ignore')
            print '> looking for: ', address
            location.address = address
            r = requests.get(self._geocode_url, params=urlencode({'sensor':'false', 'address':address}))
            if 200 == r.status_code:
                location.json = r.content
                coded = json.loads(location.json)
                if 'OK' == coded['status']:
                    location.latitude = coded['results'][0]['geometry']['location']['lat']
                    location.longitude = coded['results'][0]['geometry']['location']['lng']
                    location.accuracy = coded['results'][0]['types'][0]
                else:
                    location.accuracy = 'missing'
            print location.accuracy


    def updateLocations(self):
        locations = Location.query.filter(Location.accuracy == None).all()
        for l in locations:
            self.geocode(l)
            session.commit()
            sleep(1.5)

def processLocation(address):
    # check if already exists
    existing_location = Location.query.filter(Location.address == address).filter(Location.accuracy != None).first()
    if not existing_location:
        existing_location = Location()
        existing_location.address = address
        print '> ', address, 'unknown'
    else:
        print '> already had', address
    return existing_location
