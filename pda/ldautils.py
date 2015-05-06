import re
import string
import operator
import numpy as np 
import lda
import os
from django.conf import settings

def load_reuters():
        return ldac2dtm(open('/home/ubuntu/pda/pda/download/tweet.txt'), offset=0)


def load_reuters_vocab():
        with open('/home/ubuntu/pda/pda/download/tweet_tokens.txt') as f:
            vocab = tuple(f.read().split())
        return vocab


def load_reuters_titles():
        with open('/home/ubuntu/pda/pda/download/tweet_titles_clean.txt') as f:
            titles = tuple(line.strip() for line in f.readlines())
        return titles

def ldac2dtm(stream, offset=0):
    doclines = stream

    # We need to figure out the dimensions of the dtm.
    N = 0
    V = -1
    data = []
    for l in doclines:
        l = l.strip()
        # skip empty lines
        if not l:
            continue
        unique_terms = int(l.split(' ')[0])
        term_cnt_pairs = [s.split(':') for s in l.split(' ')[1:]]
        for v, _ in term_cnt_pairs:
            # check that format is indeed LDA-C with the appropriate offset
            if int(v) == 0 and offset == 1:
                raise ValueError("Indexes in LDA-C are offset 1")
        term_cnt_pairs = tuple((int(v) - offset, int(cnt)) for v, cnt in term_cnt_pairs)
        np.testing.assert_equal(unique_terms, len(term_cnt_pairs))
        V = max(V, *[v for v, cnt in term_cnt_pairs])
        data.append(term_cnt_pairs)
        N += 1
    V = V + 1
    dtm = np.zeros((N, V), dtype=np.intc)
    for i, doc in enumerate(data):
        for v, cnt in doc:
            np.testing.assert_equal(dtm[i, v], 0)
            dtm[i, v] = cnt
    return dtm

def preprocess(cursor, id):
    os.remove('/home/ubuntu/pda/pda/download/tweet_titles_clean.txt');
    os.remove('/home/ubuntu/pda/pda/download/tweet.txt');
    os.remove('/home/ubuntu/pda/pda/download/tweet_tokens.txt');

    # file = open('/home/ubuntu/pda/pda/download/tweet_titles.txt', 'r')
    # for tweet in file.readlines():
    #    processTweet(tweet)

    for tweet in cursor:
        tweet = tweet['text'].encode('utf-8')
        processTweet(tweet)
   
    generateldac()
    topic_list = runldamodel()
    return topic_list

def processTweet(tweet):
    tweet = tweet.lower()
    # Convert www.* or http?:// to URL
    tweet = re.sub('((www\.[\s]+)|(http?://[^\s]+))', '', tweet)
    # Convert @username to AT_USER
    tweet = re.sub('@[^\s]+', '', tweet)
    # Remove additional white sapces
    tweet = re.sub('[\s]+', ' ', tweet)
    # Replace #word with word
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    # trim
    tweet = tweet.strip('\'"')
    # Remove punctuation
    exclude = set(string.punctuation)
    tweet = ''.join(ch for ch in tweet if ch not in exclude)

    stopWords = []
    fp = open('/home/ubuntu/pda/stopwords.txt', 'r')
    line = fp.readline()
    while line:
        word = line.strip()
        stopWords.append(word)
        line = fp.readline()
    fp.close()

    tweet = ' '.join([word for word in tweet.split() if word not in stopWords])
    file = open('/home/ubuntu/pda/pda/download/tweet_titles_clean.txt', 'a')
    file.write(tweet + '\n')
    file.close()

    words = tweet.split()
    for w in words:
        w = w.strip('\'"?,.')
        # check if the word stats with an alphabet
        val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*$", w)
        if(w in stopWords or val is None):
            continue
        else:
            file = open('/home/ubuntu/pda/pda/download/tweet_tokens.txt', 'a')
            file.write(w + '\n')
            file.close()

def generateldac():
    file = open('/home/ubuntu/pda/pda/download/tweet_titles_clean.txt', 'r')
    term_dict = {}
    tokens = []
    tokens_file = open('/home/ubuntu/pda/pda/download/tweet_tokens.txt', 'r')
    for token in tokens_file.readlines():
        tokens.append(token.strip())
    tokens_file.close()

    for tweet in file.readlines():
        lenth = len(tweet.split())
        for term in tweet.split():
            if term in tokens:  
                if term not in term_dict:
                    term_dict[tokens.index(term)] = 1
                else:
                    term_dict[tokens.index(term)] = term_dict[tokens.index(term)] + 1
        file = open('/home/ubuntu/pda/pda/download/tweet.txt', 'a')
        if len(term_dict) > 0:
            file.write(str(len(term_dict)) + ' ')
            sorted_x = sorted(term_dict.items(), key=operator.itemgetter(0))
            for item in sorted_x:
                file.write(str(item[0]) + ':' + str(item[1]) + ' ')
            file.write('\n')
            file.close()
            term_dict = {}

def runldamodel():
    X = load_reuters()
    vocab = load_reuters_vocab()
    titles = load_reuters_titles()

    model = lda.LDA(n_topics=8, n_iter=1500, random_state=1)
    model.fit(X)  # model.fit_transform(X) is also available
    topic_word = model.topic_word_  # model.components_ also works
    n_top_words = 11

    topic_dict = {}
    topic_list = []
    for i, topic_dist in enumerate(topic_word):
        topic_words = np.array(vocab)[np.argsort(topic_dist)][:-n_top_words:-1]
        topic_list.append({'topic':'Topic {}: {}'.format(i, ' '.join(topic_words))})

    doc_topic_list = []
    doc_topic = model.doc_topic_
    for i in range(10):
        doc_topic_list.append("{} (top topic: {})".format(titles[i], doc_topic[i].argmax()))
    return {'topics':topic_list, 'doctopic':doc_topic_list}

