#!/usr/bin/python

# extract structured information from newly downloaded postings

from elixir import *
from operations.download import *
from models.remote import Url, Posting
from models.local import Entry


metadata.bind = "mysql://obtanium:obtanium@localhost/obtanium"
setup_all()


#config_paths = ['config/craigslist-apartment-rental.json', 'config/kijiji-apartment-rental.json']
config_paths = ['config/craigslist-apartment-rental.json']

configs = []
for c in config_paths:
    fh = open(c)
    config = json.loads(fh.read())
    fh.close()
    configs.append(config)

postings = Posting.query.filter(Posting.url.has(status='downloaded')).all()
print len(postings), 'ready for processing'
for p in postings:
    for c in configs:
        print c['url_match'] , p.url.value
        if c['url_match'] in p.url.value:
            print p.url.value
            e = Entry(c)
            e.process(p)
            break
        break
    break
#session.commit()
