import re

punctuations = [".", "\"", ",", "?", "!", "-", "(", ")", ";", ":", "\%", "$", "-", "'s", "'", "[", "]", "{", "}", "\n", "~", "_"]

def convertCamelCase(name):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1 \2', name)
        s2= re.sub('([a-z0-9])([A-Z])', r'\1 \2', s1)
        return s2

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


def preliminaryCleaning(word):
        to_delete=['&gt;', '&lt;', '&amp;', 'RT']
        word=handleUnicord(word)
        if ',' in word: word=word.replace(',', ', ')
        for mark in to_delete:
                if mark in word: word=word.replace(mark, ' ')

        return word

def isMentionOrHash(word):
        if word.startswith('@') or word.startswith('#'):
                return True

def removeSucceedingPunctuations(word):
        for punctuation in punctuations:
                if word.endswith(punctuation):
                        word=word[:word.rfind(punctuation)]
        return word

def performPreliminaryCleaning(tweet):
        cleaned_tweet=''
        for word in tweet.split():
                word=preliminaryCleaning(word)
                cleaned_tweet+=word+' '
        return cleaned_tweet

def spotMentionsAndHash(tweet):
	cleaned_tweet=''
        for word in tweet.split():
                if isMentionOrHash(word):
                        normalized_word=''
                        if '_' in word:
                                normalized_word=' '.join(word[1:].split('_'))
                        else:
                                normalized_word=convertCamelCase(word[1:].strip())

                        cleaned_tweet+=normalized_word+' '
		else:
			cleaned_tweet+=word+' '
        return cleaned_tweet



def clean_tweet(tweet):
	tweet=performPreliminaryCleaning(tweet)
	tweet=spotMentionsAndHash(tweet)
	cleaned_tweet=''
	for word in tweet.split():
		cleaned_tweet+=removeSucceedingPunctuations(word)+' '

	return cleaned_tweet



