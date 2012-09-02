import sys
from bs4 import BeautifulSoup, Comment
from bs4.element import Tag, NavigableString

# used to extract information from html structure as per config
class Extractor(object):

    def __init__(self, fields):
        self.fields = fields
        
    # returns a dictionary populated with structured information as defined in the config
    def extract(self, raw_html):
        results = {}
        data = BeautifulSoup(raw_html, 'lxml')
        for f in self.fields:
            print f['name']
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
        print 'FIND_ALL'
        data = [data]
        for d in directives:
            print 'D: ', d
            if 'tag' in d:
                if 'attrs' in d:
                    result = []
                    for dt in data:
                        result = result + dt.find_all(d['tag'], attrs=d['attrs'])
                    data = result
                    #print d, data
                else:
                    result = []
                    for dt in data:
                        result = result + dt.find_all(d['tag'])
                    data = result
                    #print d, data
            elif 'value' in d: # return text value of tag
                result = []
                for dt in data:
                    result.append(dt[d['value']])
                data = result
                #print d, data
            elif 'result' in d: # return only nth result from the result set (single object)
                idx = int(d['result'])
                if len(data) > idx:
                    data = data[idx].strip()
                else:
                    data = data[0].strip()
                #print d, data
        return data

    # apply directives until value is found, return plain text
    def find_match(self, data, directives):
        print 'FIND'
        for d in directives:
            print 'D: ', d
            class_name = 'bs{0}'.format(d.keys()[0].title())
            directive_class = getattr(sys.modules[__name__], class_name)
            directive = directive_class(d)
            data = directive.process(data)
            print data
        return data


class Directive(object):
    def __init__(self, d):
        self.d = d
        
    def process(self, data):
        return data


# return tag matching filter
class bsTag(Directive):
    def process(self, data):
        if 'attrs' in self.d:
            data = data.find(self.d['tag'], attrs=self.d['attrs'])
        else:
            data = data.find(self.d['tag'])
        return data


# return value of specified attribute inside tag
class bsValue(Directive):
    def process(self, data):
        return data[self.d['value']]


# return text contents of tag
class bsText(Directive):
    def process(self, data):
        if len(self.d['text']) > 0:
            cmd = 'data.get_text()[{0}]'.format(self.d['text'])
            return eval(cmd)
        else:
            return data.get_text()
        
# extract substring, given split delimiter char and index
class bsSplit(Directive):
    def process(self, data):
        delimiter = self.d['split'][0]
        index = int(self.d['split'][1:])
        data = data.split(delimiter)[index]
        return data
 
        
# remove any occurence of substring from string        
class bsRemove(Directive):
    def process(self, data):
        return data.replace(self.d['remove'], '')


# extract comment string containing substring
class bsComment(Directive):
    def process(self, data):
        found = False
        comments = data.find_all(text=lambda text:isinstance(text, Comment))
        for c in comments:
            if self.d['comment'] in c:
                data = c
                found = True
                break
        if not found:
            data = ''
        return data

