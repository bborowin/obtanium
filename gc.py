#!/usr/bin/python

# geocoding process

from elixir import *
from operations.geocode import Geocoder
from time import sleep

import db
db.init()

gc = Geocoder()
while(True):
    try:
        session.commit()
        gc.updateLocations()
        sleep(5)
    except Exception as e:
        print e
