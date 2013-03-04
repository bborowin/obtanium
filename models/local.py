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

    def __str__(self):
        return '{0} ({1}) @ {2},{3}'.format(self.address, self.accuracy, self.latitude, self.longitude)


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
    posted = Field(DateTime())
    config = {}

    def __init__(self, config):
        self.config = config

    # return dictionary of fields and their values extracted from raw html
    def process(self, posting):
        e = Extractor(self.config['fields'])
        return e.extract(posting.content)        
    

class RentalApartment(Entry):
    def __str__(self):
        return '${0}, {1}.5, {2} {3}'.format(self.price,self.rooms,self.location.address,self.url.value)

    location = ManyToOne('Location')
    price = Field(Integer())
    rooms = Field(Integer()) # uses QC notation sans .5
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
        try:
            self.posted = datetime.strptime(attributes['posted'], '%Y-%m-%d %I:%M%p')
        except:
            self.posted = datetime.now()
        try:
            self.rooms = 2 + int(attributes['rooms'])
        except:
            self.rooms = -1
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
        try:
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
            self.getRooms()
            posting.url.status = 'processed'
            session.commit()
        except Exception as e:
            print e

    # extract apartment size from url
    def getRooms(self):
        if '-bachelor-studio-' in self.url.value:
            self.rooms = 1
        elif '-1-bedroom-den-' in self.url.value:
            self.rooms = 3
        elif '-1-bedroom-' in self.url.value:
            self.rooms = 2
        elif 'apartments-condos-' in self.url.value:
            self.rooms = 2 + int(self.url.value.split('condos-')[1].split('-')[0])
        else:
            # invalid ad type
            self.rooms = -2


class LespacApartment(RentalApartment):
    def populate(self, posting):
        try:
            self.url = posting.url
            # get attributes directly extractable from html
            attributes = self.process(posting)
            try:
                self.price = int(attributes['price'])
            except:
                self.price = -1
            posted = datetime.now()
            self.posted = posted
            self.location = processLocation(attributes['address'])
            self.getRooms()
            posting.url.status = 'processed'
            session.commit()
        except Exception as e:
            print e


class SearchNotification(Entity):
    apt = ManyToOne('RentalApartment')
    status = Field(String(250)) # new / sent / ..
    posted = Field(DateTime())



