#!/usr/bin/python

# finds all postings matching search criteria


import sys, json
from time import sleep
from elixir import *
from operations.search import *


metadata.bind = "mysql://obtanium:obtanium@localhost/obtanium?charset=utf8"
setup_all()


config_paths = ['config/search.json']
configs = []
for c in config_paths:
    fh = open(c)
    config = json.loads(fh.read())
    fh.close()
    configs.append(config)

ls = LocationSearch()
ps = PriceSearch()
rs = RoomsSearch()
results = {}
ls.chain(configs[0]["location"],results)
ps.chain(configs[0]["price"],results)
rs.chain(configs[0]["rooms"],results)

for r in results:
    if results[r] >= 14: print results[r], r
