#
#  models representing remote data objects
#

import requests, json
from elixir import *
from elixir.entity import Entity
from bs4 import UnicodeDammit

# used to store urls
class Url(Entity):
    value = Field(String(2000))
    status = Field(String(200)) # [listed, downloaded, processed, expired]
    postings = OneToMany('Posting')

# represents individual posting
class Posting(Entity):
    url = ManyToOne('Url')
    content = Field(Text(100000)) # raw html of the downloaded posting

    def __init__(self, url=None):
        self.url = url
        
    # download the body of this posting & handle different encodings
    def download(self, url=None, mark=True):
        if None != url:
            self.url = url
        cookie = dict(area_preference = "Vlanguage=en") # todo: provide cookies in config -- this one is for kijiji only
        r = requests.get(self.url.value, cookies = cookie)
        if mark and 200 == r.status_code:
            self.url.status = 'downloaded'
        clean = UnicodeDammit(r.content)
        self.content = clean.unicode_markup.encode('utf-8')
        print '{0}: {1} [{2}]'.format(self.url.value, r.status_code, clean.original_encoding)

