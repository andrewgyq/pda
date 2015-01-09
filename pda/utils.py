from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.twitter
db_weibo = client.weibo

def get_all_collection_name(flag):
	collections = []
	if len(db.collection_names()) != 0: 
		for collection in db.collection_names():
			collections.append(str(collection))
		collections.remove('system.indexes')

	if flag == 0:
		if len(db_weibo.collection_names()) != 0: 
			for collection in db_weibo.collection_names():
				collections.append(str(collection))
			collections.remove('system.indexes')
	return collections
