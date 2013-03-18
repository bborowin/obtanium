#!/usr/bin/python

# run this script to download new postings to the repo

import sys, requests, json, elixir
from random import randint
from time import sleep
from elixir import *

import db
db.init()

from models.remote import *
from models.local import *
from operations.download import *

configs = ['config/craigslist-apartment-rental-listing.json', 'config/kijiji-apartment-rental-listing.json', 'config/kijiji-house-rental-listing.json', 'config/lespac-apartment-rental-listing.json']

# create separate session for each source
# set up source listings
sessions = {}
sources = {}
for config_path in configs:
    rsession = requests.Session()
    with open(config_path) as fh:
        config = json.loads(fh.read())
        fh.close()
    rsession.headers.clear()
    rsession.headers.update(config['http']['headers'])
    if 'cookies' in config['http']:
        for c in config['http']['cookies']:
            rsession.cookies.set(c['name'], c['value'], domain=c['domain'], path=c['path'])
    sessions[config_path] = rsession
    sources[config_path] = Listing(config)


# harvest data from sources
while(True):
    session.commit()
    for config_path in configs:
        print config_path
        sources[config_path].update(sessions[config_path])
    print '> download list exhausted - sleeping'
    sleep(120 + randint(-20,20))
