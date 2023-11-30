# -*- coding:utf-8 -*-

from datetime import date
from elasticsearch import Elasticsearch

# by default we connect to localhost:9200
es = Elasticsearch([{'host':'192.168.152.55','port':9200}])

# https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-get.html
# http://localhost:9200/my-index/test-type/5/_source
content = es.get(index="get-together", doc_type="event", id=100)
print (content['_id'], content['_source']['title'])

# $ curl -XDELETE 'http://localhost:9200/twitter/tweet/1?timeout=5m'
# content = es.delete(
#     index='bing-life',
#     doc_type="Snippet",
#     id='AVdv3B38ZkQ5cp0g9x4F'
# )
# print 'Delete', content

# https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-multi-get.html
content = es.mget(
    body={
        "docs": [
        {
            "_index": "my-index",
            "_type": "test-type",
            "_id": "5"
        },
        {
            "_index": "bing-life",
            "_type": "Snippet",
            "_id": "AVdv29i_ZkQ5cp0g9x32"
        }
        ]
    }
)['docs']

for x in content:
    print(x['_type'], x['_source']['timestamp'])

# https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-reindex.html
# es.reindex(body={
#     "source": {
#         "index": "bing"
#     },
#     "dest": {
#         "index": "old_bing"
#     }
# })

#
content = es.search(
    index='bing-life',
    doc_type="Snippet",
    body={
        'from': 0,
        'size': 5,
        'query': {
            'range': {
                'no': {
                    'from': 40, 'to': 45
                }
            }
        }
    }
)['hits']['hits']

for x in content:
    print x['_id'], x['_source']['message']


def top5():

    print "--today=%s--Top5--" % (date.today().strftime("%Y%m%d"))
    result = es.search(
        index='bing-life',
        doc_type="Snippet",
        body={
            'from': 0,
            'size': 5,
            'sort': [
                {'timestamp': {'order': 'desc'}}
            ],
            'query': {
                'range': {
                    'no': {
                        'from': 0, 'to': 5
                    }
                }
            }
        }
    )['hits']['hits']

    for item in result:
        print item['_id'], item['_source']['message']


def sourcefilter():

    print("--search-request-source-filtering--")
    result = es.search(
        index='bing-life',
        doc_type="Snippet",
        body={
            'from': 0,
            'size': 5,
            'sort': [
                {'timestamp': {'order': 'desc'}}
            ],
            '_source': ['*啄木鸟*']
        }
    )['hits']['hits']

    for item in result:
        print(item['_id'], item['_source'])


# top5
top5()

sourcefilter()

