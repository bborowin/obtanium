#!/usr/bin/python

# geocoding process

from elixir import *
from operations.geocode import Geocoder
from time import sleep

metadata.bind = "mysql://obtanium:obtanium@localhost/obtanium?charset=utf8"
setup_all()

gc = Geocoder()
while(True):
    session.commit()
    gc.updateLocations()
    print '> geocoder list exhausted - sleeping'
    sleep(5)
