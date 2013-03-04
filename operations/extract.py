import sys, re
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
            #print "f['name']", f['name']
            if 'multiple' == f['type']:
                # find all matches
                results[f['name']] = self.find_matches(data, f['directives'], verbose='verbose' in f)
            elif 'single' == f['type']:
                # find a single match
                results[f['name']] = self.find_match(data, f['directives'], verbose='verbose' in f)
            #print results[f['name']]
        return results

    # find all pieces of information matching directive chain
    def find_matches(self, data, directives, verbose=False):
        #print 'FIND_ALL'
        data = [data]
        for d in directives:
            if verbose:
                print 'D: ', d
            class_name = 'f{0}s'.format(d.keys()[0].title())
            directive_class = getattr(sys.modules[__name__], class_name)
            directive = directive_class(d)
            data = directive.process(data)
            if verbose:
                print data
        return data

    # apply directives until value is found, return plain text
    def find_match(self, data, directives, verbose=False):
        #print 'FIND'
        for d in directives:
            try:
                if verbose:
                    print 'D: ', d
                class_name = 'f{0}'.format(d.keys()[0].title())
                directive_class = getattr(sys.modules[__name__], class_name)
                directive = directive_class(d)
                data = directive.process(data)
                if verbose:
                    print data
            except:
                return None
        #print data
        return data


class Directive(object):
    def __init__(self, d):
        self.d = d
        
    def process(self, data):
        return data


# return first tag matching filter
class fTag(Directive):
    def process(self, data):
        if 'attrs' in self.d:
            data = data.find(self.d['tag'], attrs=self.d['attrs'])
        else:
            data = data.find(self.d['tag'])
        return data

# return all tags matching filter
class fTags(Directive):
    def process(self, data):
        result = []
        if 'attrs' in self.d:
            for dt in data:
                result = result + dt.find_all(self.d['tag'], attrs=self.d['attrs'])
            return result
        else:
            for dt in data:
                result = result + dt.find_all(self.d['tag'])
            return result


# return value of specified attribute inside tag
class fValue(Directive):
    def process(self, data):
        return data[self.d['value']]

# return value of specified attribute inside each tag in list
class fValues(Directive):
    def process(self, data):
        result = []
        for dt in data:
            result.append(dt[self.d['value']])
        return result


# return text contents of tag
class fResults(Directive):
    def process(self, data):
        # return only nth result from the result set (single object)
        idx = int(self.d['result'])
        if len(data) > idx:
            return data[idx].strip()
        else:
            return data[0].strip()

# return text contents of tag
class fText(Directive):
    def process(self, data):
        if len(self.d['text']) > 0:
            cmd = 'data.get_text()[{0}]'.format(self.d['text'])
            return eval(cmd).strip()
        else:
            return data.get_text().strip()
        
# extract substring, given split delimiter char and index
class fSplit(Directive):
    def process(self, data):
        delimiter = self.d['split'][0]
        index = int(self.d['split'][1:])
        data = data.split(delimiter)[index].strip()
        return data
 
        
# remove any occurence of substring from string        
class fRemove(Directive):
    def process(self, data):
        return data.replace(self.d['remove'], '')


# extract comment string containing substring
class fComment(Directive):
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


class fClean(Directive):
    def process(self, data):
        if type(data) is Tag:
            # find and remove all comments
            [c.extract() for c in data.find_all(text=lambda text:isinstance(text, Comment))]
            data = data.get_text().strip()
            data = data.replace('\n', ' ')
            data = data.replace('\t', ' ')
            # hard-strip anything that was missed
            rc = re.compile('<!--.*-->')
            data = rc.sub('', data)
        elif type(data) is NavigableString:
            data = data.string.strip()
        if None != data and type(data) is unicode:
            data = data.strip()
        return data


# retrieve specific cell from table
class fCell(Directive):
    def process(self, data):
        row = int(self.d['cell'].split(':')[0])
        col = int(self.d['cell'].split(':')[1])
        data = data.find_all('tr')[row]
        data = data.find_all('td')[col]
        return data


# retrieve previous (xN) sibling
class fPrevsibling(Directive):
    def process(self, data):
        count = int(self.d['prevsibling'])
        while count > 0:
            data = data.previousSibling
            count -= 1
        return data
