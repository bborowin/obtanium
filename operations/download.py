import json
from extract import Extractor
from models.remote import Url, Posting
from elixir import *


# represents a list of postings
class Listing(object):
    
    def __init__(self, config_path):
        fh = open(config_path)
        config = json.loads(fh.read())
        fh.close()
        self.config = config

    # retrieve postings new since last visit
    def update(self):
        next_page_url = Url(value=self.config['url'], status='index')
        page_limit = int(self.config['page_limit'])
        page_count = 1
        posting_urls = []
        e = Extractor(self.config['fields'])
        while None != next_page_url:
            listing = Posting(next_page_url)
            listing.download(mark=False)
            result = e.extract(listing.content)
            # get url of next page
            next_page_url = Url(value=result['next_page_url'], status='index')
            # make sure the url is absolute
            if 'http' not in next_page_url.value:
                next_page_url.value = self.config['url'] + next_page_url.value
            # get all new posting urls
            for posting_url in result['posting_url']:
                if Url.query.filter(Url.value == posting_url).count() > 0:
                    # signal break if a known url found
                    next_page_url = None
                else:
                    url = Url(value=posting_url, status='listed')
                    posting_urls.append(url)
            session.commit()
            page_count += 1
            # break if page limit reached
            if page_count > page_limit:
                break


# encapsulates logic for downloading & storing postings
class Retriever(object):
    
    # given a listing object, retrieve all new postings
    def scrape(self, listing):
        listing.update()
        for url in Url.query.filter(Url.status == 'listed').all():
            p = Posting(url)
            p.download()
            session.commit()
            del(p)

