import json
import sys
import re
import tldextract
import pycountry
from pprint import pprint

class stats(object):

    raw_data = None

    domain = {
            'gov': 0,
            'com': 0,
            'edu': 0,
            'org': 0,
            'net': 0,
            'ac': 0,
            'int': 0,
            'etc': 0,
            }

    def load(self, filepath):
        with open(filepath, 'r') as f:
            lines = f.read()
            self.raw_data = json.loads(lines)

    def parse(self, name):
        res = {}
        data = self.raw_data[name]
        for category, items in data['categories'].iteritems():
            res[category] = { 
                    'domain': self.domain.copy(),
                    'total_count': 0
                    }
            for title, url in items.iteritems():
                ext = tldextract.extract(url)
                suffix = ext.suffix
                tmp = self.is_international(suffix)
                if tmp:
                    res[category]['domain']['int'] += 1
                do = self.find_domain_type(suffix)
                if do:
                    res[category]['domain'][do] += 1
                if tmp or do:
                    res[category]['total_count'] += 1
        return res

    def find_domain_type(self, suffix):
        for d in self.domain.keys():
            if suffix.find(d) != -1:
                return d
        return None

    def is_international(self, suffix):
                   
        co = suffix.rfind('.')
        co = suffix[co+1:].upper()
        # Special patch for United Kingdom 
        co.replace("UK","GB")
        try:
            return pycountry.countries.get(alpha_2=co) 
        except KeyError as e:
            return None

if __name__ == "__main__":
    stat = stats()
    stat.load(sys.argv[1])
    res= stat.parse("Awesome Public Datasets")
    pprint (res)
