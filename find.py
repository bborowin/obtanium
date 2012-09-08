#!/usr/bin/python

# finds all postings matching search criteria


import sys, json
from time import sleep
from elixir import *
from operations.search import *
from models.local import RentalApartment as ra

metadata.bind = "mysql://obtanium:obtanium@localhost/obtanium?charset=utf8"
setup_all()


config_paths = ['config/search.json']
configs = []
for c in config_paths:
    fh = open(c)
    config = json.loads(fh.read())
    fh.close()
    configs.append(config)

apartments = [(r[0],0) for r in session.query(ra.id).all()]
results = [{},{}]
ls = LocationSearch()
ps = PriceSearch()
rs = RoomsSearch()
ls.chain(configs[0]["location"],results)
ps.chain(configs[0]["price"],results)
rs.chain(configs[0]["rooms"],results)
print

ids = []
buckets = {}
results=results[0]
for r in results:
    if results[r] in buckets:
        buckets[results[r]].append(r)
    else:
        buckets[results[r]] = [r]

apartments = ra.query.filter(ra.id.in_([r for r in results.keys()])).all()
for a in apartments:
    print a
for k in buckets.keys():
    print k, len(buckets[k])
#[len(buckets[i]) for i in buckets.keys()]
print 'total:', len(apartments)
