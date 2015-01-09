import sys
import json
import csv
import nltk
import formatText
import pickle
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.twitter


def getsentimentlist(cursor, user):
	words = open('/home/ubuntu/pda/AFINN-111.txt')
	scores = {}
	for line in words:
		term, score = line.split("\t")
		scores[term] = int(score)

	sentimentlist = []
	for tweet in cursor:
		tweet_text = tweet['text'].encode('utf-8').lower()
		tweet_id = tweet['id']
		created_at = tweet['created_at'][4:10]+' '+tweet['created_at'][-4:]
		sentiment = 0
		for word in tweet_text.split():
			if scores.has_key(word):
				sentiment = sentiment + scores[word]
		db[user].update({"id":tweet_id},{"$set": {"sentiment": sentiment}})

		sentiment_item = {}
		sentiment_item['value'] = sentiment
		sentiment_item['name'] = tweet['text'].encode('utf-8')
		sentiment_item['time'] = created_at
		sentimentlist.append(sentiment_item)

		# if sentimentlist.has_key(created_at):
		# 	sentimentlist[created_at] = sentimentlist[created_at] + sentiment
		# else:
		# 	sentimentlist[created_at] = sentiment

	return sentimentlist






