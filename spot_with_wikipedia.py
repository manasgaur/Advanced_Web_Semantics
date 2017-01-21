import clean_tweets as clean
import search_with_elasticsearch as search
from elasticsearch import Elasticsearch
from nltk.corpus import stopwords
import urllib2

tweet_file='../data/training/NEEL2016-training.tsv'

punctuations = [".", "\"", ",", "?", "!", "-", "(", ")", ";", ":", "\%", "$", "-", "'s", "'", "[", "]", "{", "}", "\n", "~", "_"]
stopset=set(stopwords.words('english'))

def isMentionOrHash(word):
	if word.startswith('@') or word.startswith('#'):
		return True


def performPreliminaryCleaning(tweet):
	cleaned_tweet=''
	for word in tweet.split():
		word=clean.performPreliminaryCleaning(word)
		cleaned_tweet+=word+' '
	return cleaned_tweet

def removeSucceedingPunctuations(word):
	for punctuation in punctuations:
                if word.endswith(punctuation):
                        word=word[:word.rfind(punctuation)]
	return word


def spotMentionsAndHash(tweet, es, index):
	spotted=set()
	for word in tweet.split():
		if isMentionOrHash(word):
			normalized_word=''
			if '_' in word:
                                normalized_word=' '.join(word[1:].split('_'))
			else:
				normalized_word=clean.convertCamelCase(clean.removePunctuations(word[1:])).strip()
			
			normalized_word=removeSucceedingPunctuations(normalized_word)
                	for spots in search.getExactMatches(normalized_word, es, index):
                        	spotted.add((normalized_word, (word[1:].strip(), convertOriginalPhraseToSpottedPhrase(word[1:].strip()))))
	return spotted

def removeMentionsAndHash(tweet):
	for word in tweet.split():
                if isMentionOrHash(word):
			tweet=tweet.replace(word, '')
	return tweet

def convertOriginalPhraseToSpottedPhrase(originalPhrase):
	#heuristics
	#1. if the original phrase has words that are just punctuations, delete them
	#2. if the original phrase ends with punctuations, delete them
	
	modifiedOriginal=''
	for word in originalPhrase.split(' '):
		if word.strip() not in punctuations:
			modifiedOriginal+=word+' '#originalPhrase.replace(word.strip(), '')
	modifiedOriginal=modifiedOriginal.strip()
	
	modifiedOriginal=removeSucceedingPunctuations(modifiedOriginal)
	
	return modifiedOriginal.strip()

def shouldCheckForAnchors(phrase):
	tokens=phrase.strip().lower().split(' ')
	if len(tokens)==1:
		return True
	else:
		if tokens[0].strip() in stopset or tokens[len(tokens)-1].strip() in stopset:
			return False
		else:
			return True		

def getSpottedngrams(tweet, n, matched, es):
	if not tweet.strip():
		return matched
	
	tweets_comps=tweet.split(' ')
	origin=0
        for x in range(0, len(tweets_comps)):
                searchphrase=''
		originalphrase=''
                if not x+n>len(tweets_comps):
                        for i in range(0, n):
                                searchphrase+=tweets_comps[x+i].strip()+' '
				originalphrase+=tweets_comps[x+i]+' '
                cleaned_phrase=clean.removePunctuations(searchphrase.strip())
                matches=search.getExactMatches(cleaned_phrase, es, 'natitles')
		if shouldCheckForAnchors(cleaned_phrase):
			matches|=search.getExactMatches(cleaned_phrase, es, 'nanchors')
		
		if len(matches)>0:
			matched.add((cleaned_phrase.strip(), (originalphrase.strip(), convertOriginalPhraseToSpottedPhrase(originalphrase.strip()))))
			tweet1=tweet[0:origin]
			tweet2=tweet[origin+len(originalphrase.strip()):]
			return getSpottedngrams(tweet1.strip(), n, matched, es) | getSpottedngrams(tweet2.strip(), n, matched, es)
		origin+=len(tweets_comps[x])+1
	return matched

def cleanSpottedText(tweet, spotted):
	tweet=tweet.strip()
	for spot in spotted:
		if tweet.startswith(spot[1][0]):
        	        tweet=tweet.replace(spot[1][0]+' ', ' ')
	        elif tweet.endswith(spot[1][0]):
        	        tweet=tweet.replace(' '+spot[1][0], ' ')
		else:
			tweet=tweet.replace(' '+spot[1][0]+' ', ' ')
	return tweet

def getKeyPhraseness(es, phrase):
	phrase=phrase.lower()
	total_count=float(es.count(index='wikipedia', body={ "query" : { "match_phrase" : { "text" : "\" "+phrase.strip()+" \"" }}})['count'])
	
	tokens = phrase.split()
        anchor = '+'.join(tokens)
        url = 'http://localhost:8082/anchorservice?anchor=' + anchor + '&method=getpages'
        response = eval(urllib2.urlopen(url).read())
        as_anchors=float(sum(response.values()))
	print as_anchors
	print total_count	

	return as_anchors/total_count

def spotter():
	spottedText=''
	linkableText=''
	for line in open(tweet_file).readlines():
		print line
		es = Elasticsearch()
		spotted_hash=set()
		tweet=performPreliminaryCleaning(line.split('\t')[1])
		spotted_hash|=spotMentionsAndHash(tweet, es, 'natitles')
		spotted_hash|=spotMentionsAndHash(tweet, es, 'nanchors')
		hashMentionRemoved=removeMentionsAndHash(tweet)
		URLRemoved=clean.clean_and_stem(hashMentionRemoved, 1, 0, 0)

		spotted_titles=set()
		fourgram=getSpottedngrams(URLRemoved, 4, set(), es)
		URLRemoved=cleanSpottedText(URLRemoved, fourgram)
		trigram=getSpottedngrams(URLRemoved, 3, set(), es)
                URLRemoved=cleanSpottedText(URLRemoved, trigram)
		bigram=getSpottedngrams(URLRemoved, 2, set(), es)
                URLRemoved=cleanSpottedText(URLRemoved, bigram)
		unigram=getSpottedngrams(URLRemoved, 1, set(), es)
		URLRemoved=cleanSpottedText(URLRemoved, unigram)		
		
		spotted_titles|=fourgram
		spotted_titles|=trigram
		spotted_titles|=bigram
		spotted_titles|=unigram

		spotted_anchors=set()
#		fourgram=getSpottedngrams(URLRemoved, 4, set(), es, 'nanchors')
#                URLRemoved=cleanSpottedText(URLRemoved, fourgram)
#                trigram=getSpottedngrams(URLRemoved, 3, set(), es, 'nanchors')
#                URLRemoved=cleanSpottedText(URLRemoved, trigram)
#                bigram=getSpottedngrams(URLRemoved, 2, set(), es, 'nanchors')
#                URLRemoved=cleanSpottedText(URLRemoved, bigram)
#                unigram=getSpottedngrams(URLRemoved, 1, set(), es, 'nanchors')
#                URLRemoved=cleanSpottedText(URLRemoved, unigram)
		
#		spotted_anchors|=fourgram
#		spotted_anchors|=trigram
#		spotted_anchors|=bigram
#		spotted_anchors|=unigram
		
		spotted=spotted_hash|spotted_titles|spotted_anchors
		for spot in spotted:
			if not spot[1][1] in stopset:
				spottedText+=spot[1][1]+', '
				linkableText+=spot[0]+', '

		spottedText+='\n'
		linkableText+='\n'
	f1=open('../data/training/spotted_content', 'w')
	f1.write(spottedText)
        f1.close()

	f1=open('../data/training/linkable_content', 'w')
        f1.write(linkableText)
        f1.close()

#spotter()	
es=Elasticsearch()
print getKeyPhraseness(es, 'sandra bullock')
