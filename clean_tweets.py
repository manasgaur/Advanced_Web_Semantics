import os
import re

def convertCamelCase(name):
	s1 = re.sub('(.)([A-Z][a-z]+)', r'\1 \2', name)
        s2= re.sub('([a-z0-9])([A-Z])', r'\1 \2', s1)
        return s2
#	if name.isalnum() and not name.islower():
#		s1 = re.sub('(.)([A-Z][a-z]+)', r'\1 \2', name)
#		s2= re.sub('([a-z0-9])([A-Z])', r'\1 \2', s1)
#		return s2
#	else:
#		return name

def removePunctuations(text):
	#DO NOT CHANGE THIS: THIS CLEANING IS USED FOR INDEXING THE WIKIPEDIA. CHANGING THIS WILL AFFECT THE SPOTTING THE ENTITIES
        punctuation = [".", "\"", ",", "?", "!", "-", "(", ")", ";", ":", "\%", "$", "-", "'s", "'", "[", "]", "{", "}", "\n", "~", "_"]

	for punc in punctuation:
                text = text.replace(punc, " ")

	return text

def handleUnicord(word):
	clean=word
        if not all(ord(c) < 128 for c in word):#handling 's scenario
		u=word.decode("utf-8")
		if u"\u2019" in u:
	                clean=u.replace(u"\u2019", '\'')
			clean=clean.encode('ascii', 'ignore')
			clean=clean.replace('\'s', '')
		else:
			clean="".join([s if ord(s) < 128 else '<SEP>' for s in word])
			clean=clean.replace('<SEP>', '')
	return clean
	

def performPreliminaryCleaning(word):
	to_delete=['&gt;', '&lt;', '&amp;', 'RT']
	word=handleUnicord(word)
	if ',' in word: word=word.replace(',', ', ')
        for mark in to_delete:
        	if mark in word: word=word.replace(mark, ' ')

	return word 

def clean_and_stem(line, remove_urls, normalize_digit, removePunctuation):
	# remove @mentions, URLS, twitter pics, numbers
	clean_line=''
	for word in line.split():
		if remove_urls and word.startswith("http"): word=''
		if word.startswith("@"):
			if '_' in word:
				word=' '.join(word[1:].split('_'))
			else:
				word =convertCamelCase(word[1:]).lower()
		if word.startswith('rt'): word =''
		if normalize_digit and word.isdigit(): word='NUMBER'
		if word.startswith('#'): word=convertCamelCase(word[1:]).lower()
		word=handleUnicord(word)
#		if not all(ord(c) < 128 for c in word):  word=''
		clean_line+=word+' '
	
	if removePunctuation:
		clean_line=removePunctuations(clean_line)

	return clean_line


def prepareForRitterAnnotation(file_name):
	tweets=open(file_name).readlines()
	cleaned_tweets=''
	hash_and_mentions=''
	
	for tweet in tweets:
	        tweet=tweet.split('\t')[1]
		for word in tweet.split(" "):
			if word.startswith("http"): word=''
			if word.startswith("@"):
				hash_and_mentions+=word.strip()+'$ '
	                        if '_' in word:
        	                        word=' '.join(word[1:].split('_'))
                	        else:
                        	        word =convertCamelCase(word[1:])
			if word.startswith('#'): 
				hash_and_mentions+=word.strip()+'$ '
				word=convertCamelCase(word[1:])
			word=performPreliminaryCleaning(word)

		       	cleaned_tweets+=word.strip()+' '
		cleaned_tweets+='\n'	
		hash_and_mentions+='\n'		

	writeToFile(cleaned_tweets, '<Destination file_name>')
	writeToFile(hash_and_mentions, '<Destination file_name>')

def cleanTweets(file_name):
	tweets=open(file_name).readlines()
	content_upper=''
	content_lower=''
	for tweet in tweets:
		tweet=tweet.split('\t')[1]
		cleaned_tweet=''
		for token in clean_and_stem(tweet, 1, 0, 1):
			cleaned_tweet+=token+' '
		content_upper+=cleaned_tweet.strip()+'\n'
		content_lower+=cleaned_tweet.lower().strip()+'\n'

	writeToFile(content_upper, '<Destination file_name>')
	writeToFile(content_lower, '<Destination file_name>')

def writeToFile(content, file_name):
	f1=open(file_name, 'w')
	f1.write(content)
	f1.close()

#print handleUnicord(open('temp').readlines()[0])
#prepareForRitterAnnotation('../data/training/NEEL2016-training.tsv')
