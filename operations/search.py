# search the repository of postings given a set of criteria
"""
    search for postings containing multiple attributes
    
    each attribute has a score associated with it
    postitive and negative matches: +score for matching attr, -score for explicit mismatch, +0 for no data on given attribute-posting pair

    filter by each attribute, returning a list of (postingId, score) tuples
    compile result list by summing scores for each postingid and ordering the list descending by score
"""

from elixir import *
from sqlalchemy.sql import between
from models.local import *


class AttributeSearch(object):

    # returns a list of ids matching search parameters
    def result(self, config, results):
        return []

    def chain(self, config, results):
        local = [l[0] for l in self.find(config, results)]
        for l in local:
            if l in results: results[l] += config['score']
            else: results[l] = config['score']
        return results


class LocationSearch(AttributeSearch):
    accuracies = ['bus_station', 'hospital', 'intersection', 'neighborhood', 'point_of_interest', 'postal_code', 'postal_code_prefix', 'route', 'street_address', 'subpremise', 'subway_station', 'train_station', 'university']
    
    def find(self, config, results):
        hits = []
        for t in config['targets']:
            latitude = float(t['center'][0])
            longitude = float(t['center'][1])
            radius = float(t['radius'])
            locations = session.query(Location.id).filter(Location.accuracy.in_(self.accuracies)).filter(between(Location.latitude, latitude-radius, latitude+radius)).filter(between(Location.longitude, longitude-radius, longitude+radius)).all()
            for l in locations:
                if l[0] not in hits: hits.append(l[0])
        return session.query(RentalApartment.id).filter(RentalApartment.location_id.in_(hits)).order_by(RentalApartment.price.desc()).all()


class PriceSearch(AttributeSearch):
    def find(self, config, results):
        minimum = config['min']
        maximum = config['max']
        return session.query(RentalApartment.id).filter(between(RentalApartment.price, minimum, maximum)).order_by(RentalApartment.posted.desc()).all()


class RoomsSearch(AttributeSearch):
    def find(self, config, results):
        minimum = config['min']
        maximum = config['max']
        return session.query(RentalApartment.id).filter(between(RentalApartment.rooms, minimum, maximum)).order_by(RentalApartment.posted.desc()).all()
