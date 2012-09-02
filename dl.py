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
    for c in configs:
        try:
            l = Listing(c)
            r = Retriever()
            r.scrape(l)
        except Exception as e:
            print "OOPS:", e.msg
    sleep(360 + randint(-30,30))
