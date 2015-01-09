import re

def getstatistic(cursor):
	tweets = ''
	time = {}
	source = {}
	for tweet in cursor:
		tweets = tweets + tweet['text'].encode('utf-8')
		if str(tweet['created_at'])[11:13] not in time:
			time[str(tweet['created_at'])[11:13]] = 1
		else:
			time[str(tweet['created_at'])[11:13]] = time[str(tweet['created_at'])[11:13]] + 1

		if str(tweet['source']) not in source:
			source[str(tweet['source'])] = 1
		else:
			source[str(tweet['source'])] = source[str(tweet['source'])] + 1

	all_at = re.findall('@\w+', tweets)
	all_hashtag = re.findall('#\w+', tweets)
	at_count = {}
	for at in all_at:
		if at not in at_count:
			at_count[at] = 1
		else:
			at_count[at] = at_count[at] + 1
	sorted_x = sorted(at_count, key=at_count.get, reverse=True)
	at = sorted_x[0:10]
	value = []
	for i in at:
		value.append(at_count[i])
		
	time_count = []
	time_count.append(time['00'] if time.has_key('00') else 0)
	time_count.append(time['03'] if time.has_key('03') else 0)
	time_count.append(time['06'] if time.has_key('06') else 0)
	time_count.append(time['09'] if time.has_key('09') else 0)
	time_count.append(time['12'] if time.has_key('12') else 0)
	time_count.append(time['15'] if time.has_key('15') else 0)
	time_count.append(time['18'] if time.has_key('18') else 0)
	time_count.append(time['21'] if time.has_key('21') else 0)
	time_count.append(0)

	context = {'at': at, 'value':value, 'time':time_count, 'source':source}
	return context