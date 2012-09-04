# models representing local data objects
from elixir import *
import json, requests
from operations.extract import Extractor
from models.remote import Url, Posting
from datetime import datetime


class Location(Entity):
    address = Field(String(2000))
    json = Field(Text(10000))
    
    accuracy = Field(String(50))
    latitude = Field(Float())
    longitude = Field(Float())

def processLocation(address):
    # check if already exists
    existing_location = Location.query.filter(Location.address == address).first()
    if not existing_location:
        existing_location = Location()
        existing_location.address = address
        print '> ', address, 'unknown'
    else:
        print '> already had', address
    return existing_location


# base class for processed postings
class Entry(Entity):
    url = ManyToOne('Url')
    config = {}

    def __init__(self, config):
        self.config = config

    # return dictionary of fields and their values extracted from raw html
    def process(self, posting):
        e = Extractor(self.config['fields'])
        return e.extract(posting.content)        
    

class RentalApartment(Entry):
    posted = Field(DateTime())
    location = ManyToOne('Location')
    price = Field(Integer())
    bedrooms = Field(Integer())
    floor = Field(Integer())
    appliances = Field(String(2000))
    backyard = Field(String(2000))
    balcony = Field(String(2000))


class CraigslistApartment(RentalApartment):
    def populate(self, posting):
        self.url = posting.url
        # get attributes directly extractable from html
        attributes = self.process(posting)
        try:
            self.price = int(attributes['price'])
        except:
            self.price = -1
        self.posted = attributes['posted']
        self.bedrooms = attributes['bedrooms']
        self.location = processLocation(self.getAddress(attributes))
        posting.url.status = 'processed'
        session.commit()
        
    def getAddress(self, attributes):
        if None != attributes['cross_street'] and len(attributes['cross_street'].strip()) > 0:
            address = u'{0} and {1}, {2}, {3}'.format(attributes['street'], attributes['cross_street'], attributes['city'], attributes['region']);
        else:
            address = u'{0}, {1}, {2}'.format(attributes['street'], attributes['city'], attributes['region']);
        return address


class KijijiApartment(RentalApartment):
    def populate(self, posting):
        self.url = posting.url
        # get attributes directly extractable from html
        attributes = self.process(posting)
        try:
            self.price = int(attributes['price'])
        except:
            self.price = -1
        try:
            posted = datetime.strptime(attributes['posted'], '%d-%b-%y')
        except:
            posted = datetime.now()
        self.posted = posted
        self.location = processLocation(attributes['address'])
        posting.url.status = 'processed'
        session.commit()

