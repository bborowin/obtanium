# search the repository of postings given a set of criteria
"""
    search for postings containing multiple attributes
    
    each attribute has a score associated with it
    postitive and mismatches matches: +score for matching attr, -score for explicit mismatch, +0 for no data on given attribute-posting pair

    filter by each attribute, returning a list of (postingId, score) tuples
    compile result list by summing scores for each postingid and ordering the list descending by score
"""

from elixir import *
from sqlalchemy.sql import between
from models.local import RentalApartment as ra, Location


class AttributeSearch(object):

    # returns a list of ids matching search parameters
    def find(self, config):
        return []

    def chain(self, config, results):
        lists = self.find(config)
        matches = [l[0] for l in lists[0]]
        mismatches = [l[0] for l in lists[1]]
        #print len(matches), len(mismatches)
        for m in matches:
            if m not in results[1]:
                if m in results[0]:
                    results[0][m] += config['score']
                else:
                    results[0][m] = config['score']
        for m in mismatches:
            if m in results[1]:
                results[1][m] -= config['score']
            else:
                results[1][m] = -config['score']
            if m in results[0]:
                del(results[0][m])
        return results


class LocationSearch(AttributeSearch):
    accuracies = ['bus_station', 'hospital', 'intersection', 'neighborhood', 'point_of_interest', 'postal_code', 'postal_code_prefix', 'route', 'street_address', 'subpremise', 'subway_station', 'train_station', 'university']
    
    def find(self, config):
        hits = []
        for t in config['targets']:
            latitude = float(t['center'][0])
            longitude = float(t['center'][1])
            radius = float(t['radius'])
            locations = session.query(Location.id).filter(between(Location.latitude, latitude-radius, latitude+radius)).filter(between(Location.longitude, longitude-radius, longitude+radius)).all()
            for l in locations:
                if l[0] not in hits: hits.append(l[0])
        matches = session.query(ra.id).filter(ra.location_id.in_(hits)).all()
        mismatches = session.query(ra.id).filter(~ra.location_id.in_(hits)).all()
        return matches, mismatches


class PriceSearch(AttributeSearch):
    def find(self, config):
        minimum = config['min']
        maximum = config['max']
        matches = session.query(ra.id).filter(between(ra.price, minimum, maximum)).order_by(ra.posted.desc()).all()
        mismatches = session.query(ra.id).filter(~between(ra.price, minimum, maximum)).order_by(ra.posted.desc()).all()
        return matches, mismatches


class RoomsSearch(AttributeSearch):
    def find(self, config):
        minimum = config['min']
        maximum = config['max']
        matches = session.query(ra.id).filter(between(ra.rooms, minimum, maximum)).order_by(ra.posted.desc()).all()
        mismatches = session.query(ra.id).filter(~between(ra.rooms, minimum, maximum)).order_by(ra.posted.desc()).all()
        return matches, mismatches
