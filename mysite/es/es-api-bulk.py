# -*- coding:utf-8 -*-

import json
from elasticsearch import Elasticsearch
from elasticsearch import helpers

es = Elasticsearch([{"host": "192.168.152.55", "port": 9200}])


def pretty(msg):
    return json.dumps(msg, sort_keys=True, indent=4, separators=(",", ": "))


def retrieve_group(id):
    content = es.get(index="get-together", doc_type="group-nested", id=id)
    print pretty(content)


def bulk_index_group():
    op_actions = []
    delete_action = {
        "_op_type": "delete",
        "_index": "get-together",
        "_type": "group-nested",
        "_id": 1
    }

    index_action = {
        "_index": "get-together",
        "_type": "group-nested",
        "_id": 4,
        "_source": {
            "name": "Elasticsearch News",
            "members": [
                {
                    "first_name": "Lee",
                    "last_name": "Hinman",
                }, {
                    "first_name": "Radu",
                    "last_name": "Gheorghe",
                }
            ]
        }
    }
    op_actions.append(delete_action)

    raw_result = helpers.bulk(es, actions=op_actions)
    print pretty(raw_result)

# bulk_index_group()

# retrieve_group(4)


# Multi search request for events and groups about Elasticsearch
def multi_search():
    m_query = [
        {"index": "get-together", "type": "group"},
        {
            "query": {
                "match": {
                    "name": "elasticsearch"
                }
            }
        },
        {"index": "get-together", "type": "event"},
        {
            "query": {
                "match": {
                    "title": "elasticsearch"
                }
            }
        },

    ]

    raw_result = es.msearch(body=m_query)
    print pretty(raw_result)

# multi_search()


# mget endpoint and “docs” array with index, type, and ID of documents
def multi_get():
    m_get = {
        "docs": [
            {
                "_index": "get-together",
                "_type": "group-nested",
                "_id": 1
            },
            {
                "_index": "get-together",
                "_type": "group-nested",
                "_id": 4
            }
        ]
    }
    raw_result = es.mget(body=m_get, params={"fields": "name"})
    print pretty(raw_result)

    print "when index and type is provided in the URL"
    m_get = {
        "ids": [1, 2, 4]
    }
    raw_result = es.mget(body=m_get, index="get-together", doc_type="group-nested", params={"fields": "name"})
    print pretty(raw_result)


# print pretty(multi_get())


def refresh_set():
    es.indices.put_settings(body={"index.refresh_interval": "10s"}, index="get-together")
    print es.indices.get_settings(index="get-together", name="index.refresh_interval")

refresh_set()


