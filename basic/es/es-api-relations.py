# -*- coding:utf-8 -*-

import json
from elasticsearch import Elasticsearch

es = Elasticsearch([{"host": "localhost", "port": 9200}])


def pretty(msg):
    return json.dumps(msg, sort_keys=True, indent=4, separators=(',', ': '))


def create():
    index_mapping = {
        "mappings": {
            "fruits": {
                "properties": {
                    "name": {"type": "string"},
                    "color": {"type": "string"},
                }
            }
        }
    }

    result = es.indices.create(index="fruits", body=index_mapping, params={"update_all_types": True})
    print(result)


create()


def create_document():
    document = {
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

    result = es.create(index="get-together", doc_type="group-nested", body=document, id=1)
    print(result)


# create_document()


def cross_match():
    custom_query = {
        "query": {
            "bool": {
                "must": [
                    {
                        "term": {
                            "members.first_name": "lee"
                        }
                    }, {
                        "term": {
                            "members.first_name": "radu"
                        }
                    }
                ]
            }
        }
    }
    content = es.search(index="get-together", doc_type="group-nested", body=custom_query)
    print(pretty(content))


# cross_match()


# Those documents have to contain the parent value in the URI as a parameter.
def create_parent_document():
    document = {
        "host": "Radu",
        "title": "Yet another Elasticsearch intro in Denver"
    }

    result = es.create(index="get-together", doc_type="event", body=document, id=1103, params={"parent": 2})
    print(result)


# create_parent_document()


# have to specify the _parent value
def retrieve_document():

    content = es.get(index="get-together", doc_type="event", id=1103, params={"parent": 2})
    print(pretty(content))


# retrieve_document()


def updating_document():
    document = {
        "doc": {
            "description": "Gives an overview of Elasticsearch"
        }
    }
    es.update(index="get-together", doc_type="event", body=document, id=1103, params={"parent": 2})

# updating_document()
# retrieve_document()


# If you want to search in groups hosting events about Hadoop, you can use the has_child query or filter.
def has_child_filter_query():
    custom_query = {
        "query": {
            "filtered": {
                "filter": {
                    "has_child": {
                        "type": "event",
                        "filter": {
                            "term": {
                                "title": "hadoop"
                            }
                        }

                    }
                }


            }
        }
    }
    raw_result = es.search(index="get-together", doc_type="group", body=custom_query)
    print pretty(raw_result)

# has_child_filter_query()


# has_parent query to find Elasticsearch events in Denver
def has_parent_query():
    custom_query = {
        "query": {
            "bool": {
                "must": [
                    {"term": {
                        "title": "elasticsearch"
                    }},
                    {"has_parent": {
                        "type": "group",
                        "query": {
                            "term": {
                                "location_group": "denver"
                            }
                        }
                    }}
                ]

            }
        }
    }
    raw_result = es.search(index="get-together", doc_type="event", body=custom_query)
    print(pretty(raw_result))


# has_parent_query()


def index_denormalized_members():
    mapping = {
        "member": {
            "_parent": {"type": "group"},
            "properties": {
                "first_name": {"type": "string"},
                "last_name": {"type": "string"}
            }
        }
    }

    es.indices.put_mapping(doc_type="member", body=mapping)

# index_denormalized_members()


def create_members():
    document = {
        "first_name": "Radu",
        "last_name": "Gheorghe"
    }

    result = es.create(index="get-together", doc_type="member", body=document, id=10002, params={"parent": 1})
    print result
    result = es.create(index="get-together", doc_type="member", body=document, id=10002, params={"parent": 2})
    print result

create_members()


# Searching for all the members with the same ID, which will return all the duplicates of this person
def members_query():
    custom_query = {
        "query": {
            "filtered": {
                "filter": {
                    "term": {
                        "_id": 10001
                    }
                }
            }
        },
        "fields": ["_parent"]       # We only need the _parent field from each document, so we know how to update
    }

    raw_result = es.search(index="get-together", doc_type="member", body=custom_query)
    print pretty(raw_result)

members_query()










