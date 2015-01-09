import requests
import time
from pymongo import MongoClient
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

client = MongoClient('localhost', 27017)
db = client.weibo

headers = {'Cookie': '_T_WM=9136283cc44d10a7a33629a4d4303f60; gsid_CTandWM=4u6Ke7771Groy0t0BZTX47kTp2t; SUB=_2A255h1PWDeTxGedJ71oX8S_Nzj-IHXVaiH2erDV6PUJbrdANLRfykW1AqhbW-l7WQHd8eEXPTzPPN99kdQ..; M_WEIBOCN_PARAMS=featurecode%3D20000181%26rl%3D1%26luicode%3D10000012%26lfid%3D1005051965241925_-_WEIBO_SECOND_PROFILE_WEIBO%26fid%3D1005051965241925_-_WEIBO_SECOND_PROFILE_WEIBO%26uicode%3D10000012',
           'Host':'m.weibo.cn',
           'User-Agent':'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36',
           'Accept':'application/json, text/javascript, */*; q=0.01'
           }


def getweibo(user_id):
    r = requests.get('http://m.weibo.cn/n/'+str(user_id), headers=headers)
    if r.status_code == 404:
      return 'Your input id is invalid!'

    soup = BeautifulSoup(r.text)
    containerid = soup.find_all('script')[1].get_text()[42:58]

    if containerid.isdigit():
      i = 1
      isRemove = True
      while True:
        try:
          r = requests.get('http://m.weibo.cn/page/json?containerid='+str(containerid)+'_-_WEIBO_SECOND_PROFILE_WEIBO&page='+str(i), headers=headers)
          card_group = r.json()['cards'][0]['card_group']
          for card in card_group:
              if isRemove:
                db[card['mblog']['user']['screen_name']].remove()
                isRemove = False
              db[card['mblog']['user']['screen_name']].insert(card['mblog'])
          i = i + 1
          time.sleep(1)
        except KeyError, e:
          return 'Sina Data has been saved to db.'
        except:
          continue
    else:
      return 'Your input id is invalid!'
      
      


