
import urllib2
import json
import time


def query():
    """query express num"""
    response = urllib2.urlopen("http://www.kuaidi100.com/query?type=zhongtong&postid=719518551940")
    content = response.read()
    msg = json.loads(content)
    last = msg['data'][0]
    print last['time'] + "|" + last['context']


def execute():
    """loop query"""
    while True:
        query()
        # After query, we'll pause for a moment so that we can see this happen over time
        time.sleep(60)


execute()
