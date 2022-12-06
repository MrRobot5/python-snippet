# -*- coding:utf-8 -*-

import json
from elasticsearch import Elasticsearch

es = Elasticsearch([{"host": "localhost", "port": 9200}])


def pretty(msg):
    return json.dumps(msg, sort_keys=True, indent=4, separators=(',', ': '))


def filter_query():
    custom_query = {
        "query": {
            "filtered": {
                "filter": {
                    "term": {
                        "tags.verbatim": "elasticsearch",
                        "_cache": False
                    }
                }
            }
        },
    }
    custom_query.get()

    raw_result = es.search(index="get-together", doc_type="group", body=custom_query)
    print pretty(raw_result)

# filter_query()


# Combine bitset filters in a bool filter inside an and/or/not filter
def combine_filter_query():
    custom_query = {
        "query": {
            "filtered": {
                "filter": {
                    "and": {
                        "filters": [
                            {
                                "bool": {
                                    "should": [
                                        {
                                            "term": {
                                                "tags.verbatim": "elasticsearch"
                                            }
                                        },
                                        {
                                            "term": {
                                                "members": "lee"
                                            }
                                        }
                                    ]
                                }
                            },
                            {
                                "script": {
                                    "script": "doc[\"members\"].values.size > minMembers",
                                    "params": {
                                        "minMembers": 2
                                    },
                                    "lang": "groovy"
                                }
                            }
                        ]
                    }
                }
            }
        },
    }

    raw_result = es.search(index="get-together", doc_type="group", body=custom_query)
    print pretty(raw_result)

# combine_filter_query()


def shard_query_cache():
    custom_query = {
        "aggs": {
            "top_tags": {
                "terms": {
                    "field": "tags.verbatim"
                }
            }
        }
    }

    raw_result = es.search(index="get-together", doc_type="group", body=custom_query, params={"search_type": "count", "request_cache": False})
    print pretty(raw_result)

# shard_query_cache()


def analyze_query():
    custom_query = {
        "text": "The quick Brown Foxes."
    }

    raw_result = es.indices.analyze(body=custom_query)
    print pretty(raw_result)

analyze_query()
