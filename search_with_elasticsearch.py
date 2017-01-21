from elasticsearch import Elasticsearch

noun_phrase_file='../../data/training/ritter_output/NEEL2016-training-ritter-input-processed'


def getExactMatches(search_word, es, index_name):
	matches=set()
	if not search_word:
		return matches
	#natitles
        res = es.search(index=index_name, doc_type="page", body={"from" : 0, "size" : 1000, "query": {"match_phrase": {"body": search_word.lower().strip()}}}, request_timeout=60)

        if res['hits']['total']!=0:
                for doc in res['hits']['hits']:
                        matches.add(doc['_source']['body'])

#	if not matches:
#		res = es.search(index='nanchors', doc_type="entry-type", body={"query": {"match": {"label": search_word.lower().strip()}}})
#	        if res['hits']['total']!=0:
#        	        for doc in res['hits']['hits']:
#                	        matches.add(doc['_source']['label'])
        return matches


def ngrams(input, n):
        input = input.split(' ')
        output = []
        for i in range(len(input)-n+1):
                output.append(input[i:i+n])
        return [' '.join(x) for x in output]


def getTitles(phrase):
        titles=set()
        if phrase.istitle():
                titles.add(phrase)
        else:
                for i in range(1, len(phrase.split())):
                        all_ngrams=ngrams(phrase, i)
                        ngram_titles=[ngram for ngram in all_ngrams if ngram.istitle()]
                        titles |= set(ngram_titles)
        return titles


def spotWithWikipedia():
	content=''
	for line in open(noun_phrase_file).readlines():
		noun_phrases=[noun_phrase.strip() for noun_phrase in line.split(',') if noun_phrase.strip()]
		exact_matches=set()
        	for noun_phrase in noun_phrases:
			exact_matches|=getExactMatches(noun_phrase)
			if not exact_matches:
				titles=getTitles(noun_phrase)
				for title in titles:
					exact_matches|=getExactMatches(title)
	
		for match in exact_matches:
			content+=match+', '
		content+='\n'

	f1=open('../../data/training/spotted_content', 'w')
	f1.write(content)
	f1.close()

#spotWithWikipedia()
es=Elasticsearch()
phrase='sandra bullock'
#print getExactMatches(phrase, es, 'en-wikipedia')
print len(getExactMatches(phrase, es, 'en-wikipedia'))
#print getExactMatches(phrase, es, 'nnchors')
