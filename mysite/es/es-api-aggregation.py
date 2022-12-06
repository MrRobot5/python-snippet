# -*- coding:utf-8 -*-

import json
from elasticsearch import Elasticsearch
from elasticsearch.client import IndicesClient

# by default we connect to localhost:9200
es = Elasticsearch([{"host": "192.168.152.55", "port": 9200}])
print "--ping=%s" % es.ping()


def pretty(msg):
    return json.dumps(msg, sort_keys=True, indent=4, separators=(',', ': '))


# content = es.get_source(index="get-together", doc_type="group", id=5)
# print pretty(content)

custom_query = {
    "query": {
        "filtered": {
            "query": {
                "match_all": {}
            },
            "filter": {
                "missing": {
                    "field": "reviews",
                    "existence": True,
                    "null_value": True
                }
            }

        }
    },
    "fields": ["name"]

}
# content = es.search(index="get-together", doc_type="group", body=custom_query)
# print pretty(content)

indices = IndicesClient(es)
# analyzer="ik_smart"
# content = indices.analyze(index="get-together", body="I love Bears and Fish.", analyzer="standard")

# content = indices.analyze(index="get-together", body="I love Bears and Fish.", params={
#     "filters": "lowercase,reverse",
#     "tokenizer": "whitespace"
# })

# content = indices.analyze(index="get-together", body="john.smith@example.com", params={
#     "tokenizer": "standard"
# })

# Use either snowball, porter_stem, or kstem for the filter to test it out
# content = indices.analyze(index="get-together", body="administrators", params={
#     "tokenizer": "standard",
#     "filters": "snowball"
# })


# Structure of an aggregation request
#
aggregation_query = {
    "query": {
        "range": {
            "created_on": {
                "gt": "2012-06-01",
                "lt": "2012-09-01"
            }
        }
    },
    "aggregations": {  # can be shortened to aggs
        "top_tags": {  # Give the aggregation a name
            "terms": {  # Specify the aggregation type terms
                "field": "tags.verbatim"
            }
        }
    }
}
# content = es.search(index="get-together", doc_type="group", body=aggregation_query)

# Because filters don't calculate scores and are cacheable, they're faster than their query counterparts.
# Using the filter this way is good for the overall query performance, because the filter runs first
aggregation_filter_query = {
    "size": 0,      # As we only care about aggregations, we don't ask for any result
    "query": {
        "filtered": {
            "filter": {
                "term": {
                    "location_group": "denver"
                }
            }
        }
    },
    "aggregations": {  # can be shortened to aggs
        "top_tags": {  # Give the aggregation a name
            "terms": {  # Specify the aggregation type terms
                "field": "tags.verbatim"
            }
        }
    }
}

aggregation_stats_script_query = {
    "size": 0,
    "aggregations": {
        "attendees_stats": {
            "stats": {
                "script": "doc['"'attendees'"'].values.size"
            }
        }
    }
}

# you can get the other metrics through the avg, min, max, sum
aggregation_stats_avg_script_query = {
    "size": 0,
    "aggregations": {
        "attendees_avg": {
            "avg": {
                "script": "doc['"'attendees'"'].values.size"
            }
        }
    }
}
# content = es.search(index="get-together", doc_type="event", body=aggregation_stats_avg_script_query)

aggregation_extended_stats_script_query = {
    "size": 0,
    "aggregations": {
        "attendees_stats": {
            "extended_stats": {
                "script": "doc['"'attendees'"'].values.size"
            }
        }
    }
}
# content = es.search(index="get-together", doc_type="event", body=aggregation_extended_stats_script_query)
# print pretty(content)


# Getting the 80th and the 90th percentile from the number of attendees
def percentiles():
    query_params = {
        "size": 0,
        "aggregations": {
            "attendees_percentiles": {
                "percentiles": {
                    "script": "doc['"'attendees'"'].values.size",
                    "percents": [80, 99]
                }
            }
        }
    }
    raw_result = es.search(index="get-together", doc_type="event", body=query_params)
    print pretty(raw_result)

# percentiles()


def cardinality():
    query_params = {
        "size": 0,
        "aggregations": {
            "members_cardinality": {
                "cardinality": {
                    "field": "location_group"
                }
            }
        }
    }
    raw_result = es.search(index="get-together", doc_type="group", body=query_params)
    print pretty(raw_result)

# cardinality()


# A terms aggregations can be used to get term frequencies and generate a word cloud
def term_aggregations():
    query_params = {
        "size": 0,
        "aggregations": {
            "tags": {
                "terms": {
                    "field": "tags.verbatim",
                    "include": ".*search.*",    # only for terms containing "search"
                    "order": {
                        "_term": "asc"
                    }
                }
            }
        }
    }
    raw_result = es.search(index="get-together", doc_type="group", body=query_params)
    print pretty(raw_result)

# term_aggregations()


def sign_term_aggregations():
    query_params = {
        "size": 0,
        "query": {
            "match": {
                "attendees": "Lee"          # Foreground documents are events Lee attends to
            }
        },
        "aggregations": {
            "significant_attendees": {
                "significant_terms": {
                    "field": "attendees",   # We need attendees that appear more in these events than overall
                    "min_doc_count": 2,     # Take only attendees that participated to at least 2 events
                    "exclude": "lee"        # Exclude Lee from the analyzed terms, he has the same taste as himself
                }
            }
        }
    }
    raw_result = es.search(index="get-together", doc_type="event", body=query_params)
    print pretty(raw_result)

# sign_term_aggregations()


#  Using a range aggregation to divide events by the number of attendees
def range_aggregations():
    query_params = {
        "size": 0,
        "aggregations": {
            "attendees_breakdown": {
                "range": {
                    "script": "doc['"'attendees'"'].values.size",
                    "ranges": [
                        {"to": 4},
                        {"from": 4, "to": 6},
                        {"from": 6}
                    ]
                }
            }
        }
    }
    raw_result = es.search(index="get-together", doc_type="event", body=query_params)
    print pretty(raw_result)

# range_aggregations()


#  Using a date range aggregation to divide events by scheduled date
def date_range_aggregations():
    query_params = {
        "size": 0,
        "aggregations": {
            "dates_breakdown": {
                "date_range": {
                    "field": "date",
                    "format": "YYYY.MM",
                    "ranges": [
                        {"to": "2013.05"},
                        {"from": "2013.05", "to": "2013.07"},
                        {"from": "2013.07"}
                    ]
                }
            }
        }
    }
    raw_result = es.search(index="get-together", doc_type="event", body=query_params)
    print pretty(raw_result)

# date_range_aggregations()


# Histogram showing the number of events for each number of attendees
def histogram_aggregations():
    query_params = {
        "size": 0,
        "aggregations": {
            "attendees_histogram": {
                "histogram": {
                    "script": "doc['"'attendees'"'].values.size",
                    "interval": 1
                }
            }
        }
    }
    raw_result = es.search(index="get-together", doc_type="event", body=query_params)
    print pretty(raw_result)

# histogram_aggregations()


# Histogram of events per month
def date_histogram_aggregations():
    query_params = {
        "size": 0,
        "aggregations": {
            "date_histogram": {
                "date_histogram": {
                    "field": "date",
                    "interval": "1M"
                }
            }
        }
    }
    raw_result = es.search(index="get-together", doc_type="event", body=query_params)
    print pretty(raw_result)

# date_histogram_aggregations()


#
def multi_aggregations():
    query_params = {
        "size": 0,
        "aggregations": {
            "top_tags": {
                "terms": {
                    "field": "tags.verbatim"
                },
                "aggregations": {
                    "group_per_month": {
                        "date_histogram": {
                            "field": "created_on",
                            "interval": "1M"
                        },
                        "aggregations": {
                            "number_of_numbers": {
                                "range": {
                                    "script": "doc['"'members'"'].values.size",
                                    "ranges": [
                                        {"to": 3},
                                        {"from": 3}
                                    ]
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    raw_result = es.search(index="get-together", doc_type="group", body=query_params)
    print pretty(raw_result)

# multi_aggregations()


# Global aggregation helps show top tags overall regardless of the query
def global_aggregations():
    query_params = {
        "size": 0,
        "query": {
            "match": {
                "name": "elasticsearch"
            }
        },
        "aggregations": {
            "all_documents": {          # The global aggregation is the parent
                "global": {},
                "aggregations": {
                    "top_tags": {
                        "terms": {      # The terms aggregation is nested under it, to work on all data
                            "field": "tags.verbatim"
                        }
                    }
                }
            }
        }
    }
    raw_result = es.search(index="get-together", doc_type="group", body=query_params)
    print pretty(raw_result)

global_aggregations()






