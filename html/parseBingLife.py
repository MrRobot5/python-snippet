

import urllib2
from HTMLParser import HTMLParser
from datetime import date
import time
from elasticsearch import Elasticsearch

# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.tag = False
        self.content = ''

    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            find = False
            for attr, value in attrs:
                if attr == 'id' and value == 'hplaSnippet':
                    find = True
            if find:
                self.tag = True
                print("Encountered a start tag:", attrs)

    def handle_data(self, data):
        if self.tag:
            print("Encountered some data  :", data)
            self.content = data
            self.tag = False

# instantiate the parser and fed it some HTML
parser = MyHTMLParser()
# by default we connect to localhost:9200
es = Elasticsearch()

today = date.today()
for x in range(0, 30 * 12):

    # Formatting datetime
    suffix = today.strftime("%Y%m%d")
    print("request day:", suffix)
    response = urllib2.urlopen('http://cn.bing.com/cnhp/life?currentDate={0}'.format(suffix))
    content = response.read()
    parser.feed(content)

    # Calculate date
    # if today.day == 1:
    #     today = today.replace(month=today.month - 1, day=30)
    today = today.replace(day=today.day - 1)
    # wait
    time.sleep(1)

    es.index(index="bing-life", doc_type="Snippet", body={"message": parser.content, "timestamp": today, 'no': x})

