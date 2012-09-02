#
#  models representing remote data objects
#

import requests, json
from elixir import *
from elixir.entity import Entity


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
        
    # download the body of this posting
    def download(self, url=None, mark=True):
        if None != url:
            self.url = url
        r = requests.get(self.url.value)
        if mark and 200 == r.status_code:
            self.url.status = 'downloaded'
        self.content = r.content
        print '{0}: {1}'.format(self.url.value, r.status_code)

