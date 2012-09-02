# models representing local data objects
from elixir import *
import json
from operations.extract import Extractor
from models.remote import Url, Posting


class Location(Entity):
    address = Field(String(2000))
    precision = Field(Integer())
    latitude = Field(Float())
    longitude = Field(Float())

    # use geocoding service to obtain lat/lon from address
    def geocode(address = None):
        if None != address:
            self.address = address
        pass


# base class for processed postings
class Entry(Entity):
    attributes = {}
    config = {}

    def __init__(self, config):
        self.config = config

    def process(self, posting):
        e = Extractor(self.config['fields'])
        result = e.extract(posting.content)
        print result
        


class Rental(Entry):
    location = ManyToOne('Location')
    price = Field(String(2000))

    pass
