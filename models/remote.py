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
        super(Posting, self ).__init__()
        self.url = url
        self.config = config
