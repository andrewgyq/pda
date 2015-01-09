# zheng ze handle the txt
from nltk.stem.porter import *
import re
import nltk
import string
import csv
# strat process tweet


def processTweet(tweet):
    tweet = tweet.lower()
    # Convert www.* or http?:// to URL
    tweet = re.sub('((www\.[\s]+)|(http?://[^\s]+))', 'URL', tweet)
    # Convert @username to AT_USER
    tweet = re.sub('@[^\s]+', 'AT_USER', tweet)
    # Remove additional white sapces
    tweet = re.sub('[\s]+', ' ', tweet)
    # Replace #word with word
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    # trim
    tweet = tweet.strip('\'"')
    return tweet

# def processTweet(tweet):
# 	tweet=tweet.lower()
# 	no_punctuation = lowers.translate(None, string.punctuation)
#     tokens = nltk.word_tokenize(no_punctuation)
#     return tokens

# initialize stopWords
stopWords = []
# haaaapy to happy


def replaceTwoOrMore(s):
    pattern = re.compile(re.compile(r"(.)\1{1,}", re.DOTALL))
    return pattern.sub(r"\1\1", s)


def getStopWordList(stopWordListFileName):
    stopWords = []
    stopWords.append('AT_USER')
    stopWords.append('URL')

    stopWords.append('twitter')
    stopWords.append('rt')

    fp = open(stopWordListFileName, 'r')
    line = fp.readline()
    while line:
        word = line.strip()
        stopWords.append(word)
        line = fp.readline()
    fp.close()
    return stopWords


def getFeatureVector(tweet, stopWords):
    featureVector = []
    # split tweet into words
    # words1=nltk.word_tokenize(tweet)
    # print words1
    words = tweet.split()
    # print words
    for w in words:
        w = replaceTwoOrMore(w)
        w = w.strip('\'"?,.')
        # check if the word stats with an alphabet
        val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*$", w)
        if(w in stopWords or val is None):
            continue
        else:
            featureVector.append(w.lower())
    return featureVector
