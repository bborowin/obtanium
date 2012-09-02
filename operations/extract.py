from bs4 import BeautifulSoup, Comment

# used to extract information from html structure as per config
class Extractor(object):

    def __init__(self, fields):
        self.fields = fields
        
    # returns a dictionary populated with structured information as defined in the config
    def extract(self, raw_html):
        results = {}
        data = BeautifulSoup(raw_html, 'lxml')
        for f in self.fields:
            if 'multiple' == f['type']:
                results[f['name']] = []
                # find all matches
                results[f['name']] = self.find_matches(data, f['directives'])
            elif 'single' == f['type']:
                results[f['name']] = None
                # find a single match
                results[f['name']] = self.find_match(data, f['directives'])
        return results

    # find all pieces of information matching directive chain
    def find_matches(self, data, directives):
        #print 'FIND_ALL'
        data = [data]
        for d in directives:
            #print 'D: ', d
            if 'tag' in d:
                if 'attrs' in d:
                    result = []
                    for dt in data:
                        result = result + dt.find_all(d['tag'], attrs=d['attrs'])
                    data = result
                else:
                    result = []
                    for dt in data:
                        result = result + dt.find_all(d['tag'])
                    data = result
            elif 'value' in d:
                result = []
                for dt in data:
                    result.append(dt[d['value']])
                data = result
        return data

    # apply directives until value is found
    def find_match(self, data, directives):
        #print 'FIND'
        for d in directives:
            #print 'D: ', d
            if 'tag' in d:
                if 'attrs' in d:
                    data = data.find(d['tag'], attrs=d['attrs'])
                else:
                    data = data.find(d['tag'])
            elif 'value' in d:
                data = data[d['value']]
        return data
