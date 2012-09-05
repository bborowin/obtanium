#!/usr/bin/python

# extract structured information from newly downloaded postings
import sys
from time import sleep
from elixir import *
from operations.download import *
from models.remote import Url, Posting
from models.local import CraigslistApartment, KijijiApartment


metadata.bind = "mysql://obtanium:obtanium@localhost/obtanium?charset=utf8"
setup_all()


config_paths = ['config/craigslist-apartment-rental.json', 'config/kijiji-apartment-rental.json']
configs = []
for c in config_paths:
    fh = open(c)
    config = json.loads(fh.read())
    fh.close()
    configs.append(config)

postings = None
while True:
    session.commit()
    postings = Posting.query.join(Posting.url).filter(Url.status=='downloaded').all()
    if len(postings) > 0:
        print len(postings), 'ready for processing'
        for p in postings:
            for c in configs:
                if c['url_match'] in p.url.value:
                    print p.url.value
                    local_class = getattr(sys.modules[__name__], c['class'])
                    e = local_class(c)
                    e.populate(p)
                    break
            session.commit()
            session.expire(p)
        print '> extract list exhausted - sleeping'
    sleep(5)
