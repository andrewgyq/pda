# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
import json
from pymongo import MongoClient
from pymongo import Connection	
import time
import operator
from twitter import twitterreq
from sentiment import getsentimentlist
from statistic import getstatistic
from wordcloud import getwordcounts
from weibo import getweibo
from twitter import gettwitter
from utils import get_all_collection_name
from ldautils import preprocess

client = MongoClient('localhost', 27017)
db = client.twitter
db_weibo = client.weibo

def test(request):
	return render(request, 'ldatest.html')

def index(request):
	return render(request, 'index.html')

def crawl(request):
	return render(request, 'crawl.html')

def data(request):
	collections = get_all_collection_name(0)
	json_data = json.dumps({'titles': collections})
	return render(request, 'data.html', {'collections' : json_data})

def save(request):
	twitter_id = request.GET.get('id')
	info = gettwitter(twitter_id)
	return HttpResponse(info)

def get_data(request):
	page = int(request.GET.get('page',1)) 
	rows = int(request.GET.get('rows',20)) 
	id = request.GET.get('id')

	begin = (page - 1) * rows
	end = begin + rows

	cursor = db[id].find(fields = {'_id': False, 'text': True, 'created_at': True, 'sentiment': True}).sort("id",-1)
	total = cursor.count()

	if total == 0:
		cursor = db_weibo[id].find(fields = {'_id': False, 'text': True,  'sentiment': True}).sort("id",-1)
		total = cursor.count()

	tweets = []
	for tweet in cursor:
		tweets.append(tweet)
    
	data = {'total':total, 'rows':tweets[begin:end]}
	return HttpResponse(json.dumps(data))

def sentiment(request):
	collections = get_all_collection_name(1)
	json_data = json.dumps({'titles': collections})
	return render(request, 'sentiment.html', {'collections':json_data})

	
def get_sentiment(request):
	twitter_id = request.GET.get('id')
	cursor = db[twitter_id].find(fields = {'_id': False, 'text': True, 'created_at': True, 'id': True}).sort("id",-1)
	sentimentlist = getsentimentlist(cursor, twitter_id)
	return HttpResponse(json.dumps(sentimentlist)) 

def wordcloud(request):
	collections = get_all_collection_name(1)
	json_data = json.dumps({'titles': collections})
	return render(request, 'wordcloud.html', {'collections':json_data})

def get_wordcloud(request):
	twitter_id = request.GET.get('id')
	cursor = db[twitter_id].find(fields = {'_id': False, 'text': True})
	wordcounts = getwordcounts(cursor)
	return HttpResponse(wordcounts)

def statistic(request):
	collections = get_all_collection_name(1)
	json_data = json.dumps({'titles': collections})
	return render(request, 'statistic.html', {'collections':json_data})

def get_statistic(request):
	twitter_id = request.GET.get('id')
	cursor = db[twitter_id].find(fields = {'_id': False, 'text': True, 'created_at': True, 'source':True})
	context = getstatistic(cursor)
	return HttpResponse(json.dumps(context))

def lda(request):
	collections = get_all_collection_name(1)
	json_data = json.dumps({'titles': collections})
	return render(request, 'lda.html', {'collections':json_data})

def get_lda(request):
	twitter_id = request.GET.get('id')
	cursor = db[twitter_id].find(fields = {'_id': False, 'text': True})
	topic_list = preprocess(cursor, twitter_id)
	return HttpResponse(json.dumps(topic_list))

def savesina(request):
	weibo_id = request.GET.get('id')
	weibos = getweibo(weibo_id)
	return HttpResponse(weibos)

def removedb(request):
	c = Connection()
	c.drop_database('twitter')
	c.drop_database('weibo')
	return HttpResponse('success!')
	









	