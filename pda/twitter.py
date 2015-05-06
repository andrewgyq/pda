import oauth2 as oauth
import urllib2 as urllib
from pymongo import MongoClient
import time
import json

api_key = "lBlXLy8Brn6UVk0rNf0h307pR"
api_secret = "rgrdp3DOsXaIHgh4vcJH7NerR4T5NnIrBBHEhBSLzDXcslVOIs"
access_token_key = "221974821-KEwtbZt4S34hBrLm2G1dal0sQTGJxgk6zQbuA3Ey"
access_token_secret = "gpRr8jCtbb8oLedZisehn3xmbdArR1GuL5EN9HhrOiygH"

_debug = 0

oauth_token    = oauth.Token(key=access_token_key, secret=access_token_secret)
oauth_consumer = oauth.Consumer(key=api_key, secret=api_secret)

signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

http_method = "GET"


http_handler  = urllib.HTTPHandler(debuglevel=_debug)
https_handler = urllib.HTTPSHandler(debuglevel=_debug)

client = MongoClient('localhost', 27017)
db = client.twitter

def twitterreq(url, method, parameters):
  req = oauth.Request.from_consumer_and_token(oauth_consumer,
                                             token=oauth_token,
                                             http_method=http_method,
                                             http_url=url, 
                                             parameters=parameters)

  req.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)

  headers = req.to_header()

  if http_method == "POST":
    encoded_post_data = req.to_postdata()
  else:
    encoded_post_data = None
    url = req.to_url()

  opener = urllib.OpenerDirector()
  opener.add_handler(http_handler)
  opener.add_handler(https_handler)

  response = opener.open(url, encoded_post_data)

  return response

def gettwitter(id):
  return_number = 200
  flag = True
  max_id = 0

  db[id].remove()
  while return_number > 0:
    if flag :
      url = "https://api.twitter.com/1.1/statuses/user_timeline.json?count=200&screen_name="+str(id)
    else:
      url = "https://api.twitter.com/1.1/statuses/user_timeline.json?count=200&max_id="+str(max_id)+"&screen_name="+str(id)
    flag = False
    response = twitterreq(url, "GET", [])
    json_obj = json.load(response)
    return_number = len(json_obj)
    if return_number > 0:
        db[id].insert(json_obj)
        max_id = json_obj[-1]['id']-1
    time.sleep(2)
  return 'Twitter Data has been saved to db.'