from elixir import *
from bs4 import UnicodeDammit
from extract import Extractor

from models.remote import Url, Posting

# represents a list of postings
class Listing(object):
    
    def __init__(self, config):
        self.config = config

    # retrieve postings new since last visit
    def update(self, rsession):
        url = self.config['url']
        page_limit = int(self.config['page_limit'])
        page_count = 1
        posting_urls = []
        e = Extractor(self.config['fields'])
        while None != url:
            # download listing
            r = rsession.get(url)
            for c in r.cookies:
                rsession.cookies.set_cookie(c)
            clean = UnicodeDammit(r.content)
            content = clean.unicode_markup.encode('utf-8')
            print 'DL: {0}: {1} [{2}], {3} bytes'.format(url, r.status_code, clean.original_encoding, len(content))
            # pull information from html
            result = e.extract(content)
            # get url of next page
            url = result['next_page_url']
            if None == url:
                break
            # make sure the url is absolute
            if 'http' not in url:
                url = self.config['base_url'] + url
            # get all new posting urls
            new_urls = 0
            for posting_url in result['posting_url']:
                if 'http' not in posting_url:
                    posting_url = self.config['base_url'] + posting_url;
                # save any previously unseen urls
                if not Url.query.filter(Url.value == posting_url).count() > 0:
                    new_urls += 1
                    posting_urls.append(Url(value=posting_url, status='listed'))
            session.commit()
            page_count += 1
            # break if page limit reached, or page full of known urls
            if 0 == new_urls or page_count > page_limit:
                break
        print '{0} new urls found'.format(new_urls)
