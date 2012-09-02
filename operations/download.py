import json
from extract import Extractor
from models.remote import Posting
from elixir import *


# represents a list of postings
class Listing(object):
    
    def __init__(self, config_path):
        fh = open(config_path)
        config = json.loads(fh.read())
        fh.close()
        self.config = config

    # list all the postings new since last visit
    @property
    def posting_urls(self):
        next_page_url = self.config['url']
        page_limit = int(self.config['page_limit'])
        page_count = 1
        posting_urls = []
        e = Extractor(self.config['fields'])
        while None != next_page_url:
            listing = Posting(next_page_url)
            listing.download()
            result = e.extract(listing.content)
            listing.delete()
            # get url of next page
            next_page_url = result['next_page_url']
            # make sure the url is absolute
            if 'http' not in next_page_url:
                next_page_url = self.config['url'] + next_page_url
            # get all new posting urls
            for posting_url in result['posting_url']:
                if Posting.query.filter(Posting.url == posting_url).count() > 0:
                    next_page_url = None
                else:
                    posting_urls.append(posting_url)
            page_count += 1
            if page_count > page_limit:
                break
        return posting_urls


# encapsulates logic for downloading & storing postings
class Retriever(object):
    
    # given a listing object, retrieve all new postings
    def scrape(self, listing):
        for url in listing.posting_urls:
            p = Posting(url)
            p.download()
            session.commit()
            del(p)

