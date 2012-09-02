#!/usr/bin/python
from elixir import *
from operations.download import *

metadata.bind = "mysql://obtanium:obtanium@localhost/obtanium"
metadata.bind.echo = False
setup_all()

l = Listing('config/craigslist-apartment-rental-listing.json')
r = Retriever()
r.scrape(l)
