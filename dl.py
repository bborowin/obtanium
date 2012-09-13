#!/usr/bin/python

# run this script to download new postings to the repo


from elixir import *
from operations.download import *
from random import randint
from time import sleep


metadata.bind = "mysql://obtanium:obtanium@localhost/obtanium"
metadata.bind.echo = False
setup_all()

configs = ['config/craigslist-apartment-rental-listing.json', 'config/kijiji-apartment-rental-listing.json']
while(True):
    session.commit()
    for c in configs:
        l = Listing(c)
        r = Retriever()
        try:
            r.scrape(l)
        except:
            sleep(60)
    print '> download list exhausted - sleeping'
    sleep(120 + randint(-20,20))
