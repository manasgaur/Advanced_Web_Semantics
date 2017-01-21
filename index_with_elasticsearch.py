from pyelasticsearch.client import ElasticSearch
import clean_tweets as clean

#created indices: titles - analyzed, anchors - analyzed, natitles - not analyzed, nanchors - not analyzed

entry_mapping = {
    'entry-type': {
        'properties': {
            'label': {'type': 'string', 'index': 'not_analyzed'},
            'canonical': {'type': 'string'}
        }
    }
}

es=ElasticSearch()  # use default of localhost, port 9200
es.create_index('natitles', settings={'mappings': entry_mapping})

titles=open('../data/dbpedia/dbpedia_names_title_map').readlines()

index_id=1
for title in titles:
	title=title.split('\t')[1].strip()
	doc={'label': clean.removePunctuations(title.strip().lower()),
		'canonical': title.strip()}
	es.index('natitles', 'entry-type', doc, id=index_id)
	index_id+=1

print 'Titles Done'

#es.create_index('nanchors', settings={'mappings': entry_mapping})
#for line in open('../data/dbpedia/anchor_text').readlines():
#	doc={'label': clean.removePunctuations(line.strip().lower()),
#		'canonical': line.strip()}
#        es.index('nanchors', 'entry-type', doc, id=index_id)
#        index_id+=1

