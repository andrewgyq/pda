# -*- coding: utf-8 -*-
import nltk
import string
from nltk.corpus import stopwords
from collections import Counter
import re
import json

def getwordcounts(cursor):
	tweets = ''
	for tweet in cursor:
		tweets = tweets + tweet['text'].encode('utf-8')
	
	no_http = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', tweets)
	no_at = re.sub('@\w+', '', no_http)
	no_sharp = re.sub('#\w+', '', no_at)
	lowers = no_sharp.lower()

	#remove the punctuation using the character deletion step of translate
	no_punctuation = lowers.translate(None, string.punctuation)
	no_punctuation0 = re.sub('(?:“|”|’|…|–)', '', no_punctuation)
	tokens = nltk.word_tokenize(no_punctuation0)

	filtered = [w for w in tokens if not unicode(w,"utf-8") in stopwords.words('english')]
	count = Counter(filtered)
	wordcounts = []
	for word in count.most_common(50):
		wordcout = {}
		wordcout['text'] = word[0]
		wordcout['size'] = word[1]
		wordcounts.append(wordcout)
	return json.dumps(wordcounts)	




