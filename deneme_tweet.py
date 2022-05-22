
import tweepy
import key
from binance.client import Client
import pandas as pd
import send_msg as tele
import time
import gspread

def tweet_coint():
    time.sleep(60)
    auth = tweepy.OAuth1UserHandler(consumer_key=key.consumer_key, consumer_secret=key.consumer_secret)
    api = tweepy.API(auth)
    username = 'coinytics'
    tweets_list = api.user_timeline(screen_name=username, count=2)
    tweet_last = tweets_list[0]
    tweet = tweet_last.id
    print (tweet)
    x = tweet_last.text
    n = x.split()
    print(n)
    situation_cross = n[1]



    if situation_cross =='Moving':
        symbol_tweet = n[11]
        position_side = n[19]
        print(symbol_tweet)
        print(position_side)
    elif situation_cross =='MA':
        symbol_tweet = n[11]
        position_side = n[19]
        print(symbol_tweet)
        print(position_side)
    else:
        print('notning')

while True:
    tweet_coint()
