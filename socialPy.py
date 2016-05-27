__author__ = 'agrimasthana'

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import sys
import time
import httplib
import urllib
import mysql.connector
import json
import multiprocessing


def setup():
    global access_token
    global access_token_secret
    global consumer_key
    global consumer_secret
    global dbconfig
    access_token = config['access_token']
    access_token_secret = config['access_token_secret']
    consumer_key = config['consumer_key']
    consumer_secret = config['consumer_secret']
    dbconfig = config['config']


def getsentiment(text):
    connection = httplib.HTTPConnection('text-processing.com', 80, timeout=30)
    body_params = {"text": text}
    body = urllib.urlencode(body_params)
    connection.request('POST', '/api/sentiment/', body, {})

    try:
        response = connection.getresponse()
        content = response.read()
        res = json.loads(content)
        return res['label']
    except httplib.HTTPException, e:
        print('Exception during request:{0}', e)


class StdOutListener(StreamListener):

    def __init__(self):
        super(StdOutListener, self).__init__()
        self.num_tweets = 0

    def on_data(self, raw_data):
        self.num_tweets += 1
        # print(self.num_tweets)

        if self.num_tweets < 30:
            write2db(raw_data)
            return True
        else:
            print('\ndone')
            sys.exit()
        # print raw_data


    def on_error(self, status_code):
        print status_code
        time.sleep(900)


def write2db(raw_data):
    try:
        tweets = json.loads(raw_data)
        # lulz
        if "Emma" in tweets['text']:
            print('Emma Watson tweet')

        sentiment = getsentiment(tweets['text'].replace('"', '').encode('utf-8').strip())
        print(tweets['user']['screen_name']+': '+tweets['text']+'\n Sentiment:'+sentiment)
        tweetdata = (tweets['user']['screen_name'], tweets['text'], sentiment)
        csr = cnx.cursor()
        csr.execute("insert into Tweets(username,tweet,sentiment) Values (%s,%s,%s)", tweetdata)
        cnx.commit()
        csr.close()
        print("Tweet Saved :-)")
    except Exception as Ex:
        print Ex
        return False

    return True


def minetweets():
    line = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, line)
    # stream.filter(track=['Watson', 'Cognitive', 'Machine Learning'])
    stream.filter(track=args, languages=["en"])


if __name__ == '__main__':
    config = {}
    execfile("settings.conf", config)
    setup()
    # Sample database logic
    try:
        cnx = mysql.connector.connect(**dbconfig)
    except Exception as E:
        print E

    # Twitter Stuff
    del sys.argv[0]
    args = sys.argv
    print 'Arguments List:', args

    miner = multiprocessing.Process(target=minetweets())
    miner.start()
    time.sleep(10)
    sys.exit()
    # line = StdOutListener()
    # auth = OAuthHandler(consumer_key, consumer_secret)
    # auth.set_access_token(access_token, access_token_secret)
    # stream = Stream(auth, line)
    # # stream.filter(track=['Watson', 'Cognitive', 'Machine Learning'])
    # stream.filter(track=args, languages=["en"])
