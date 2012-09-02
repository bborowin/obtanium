#
#  models representing remote data objects
#

import requests, json
from elixir import *
from elixir.entity import Entity



# represents individual posting
class Posting(Entity):
    url = Field(String(2000))
    content = Field(Text(100000)) # raw html of the downloaded posting

    def __init__(self, url=None):
        self.url = url
        
    # download the body of this posting
    def download(self, url=None):
        if None != url:
            self.url = url
        r = requests.get(self.url)
        self.content = r.content
        print '{0}: {1}'.format(self.url, r.status_code)

