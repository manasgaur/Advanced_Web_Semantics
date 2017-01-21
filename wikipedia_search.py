from elasticsearch import Elasticsearch

es=Elasticsearch(timeout=3000)

#print es.search(index='natitles', doc_type="entry-type", body={"query": {"match": {"label": 'barack obama'}}})

res=es.search(index='wikipedia', body={ "query" : { "match_phrase" : { "text" : "sandra bullock" }}, "size":"1000"})
print res['hits']
#res=es.search(index="twitter", body={"query": {"query_string": {"query": "sujan"}},"aggs" : {"count_terms": {"terms" : {"field" : "message", "include" : "sujan"}}}})

#res=es.search(index="twitter", body={"size": 0,"query": {"filtered": {"query": {"query_string": {"query": "*","analyze_wildcard": "true"}}}},	"aggs" : {"count_terms": {"terms" : {"field" : "text", "include" : "test"}}}})
#print res
#print  res['hits']['total']

