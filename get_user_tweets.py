

import tweepy

from binance.client import Client
import math


import time

import key
import send_msg as tele

liste_id=['0']



def signal():
    global price_sell_new

    time.sleep(15)
    client = Client(api_key=key.Pkey, api_secret=key.Skey)
    result = client.futures_account_balance(asset='USDT') # bir listeden asset cektik
    balance = float(result[6]['withdrawAvailable']) #with drawal codu ile aldık
    print (balance)
    auth = tweepy.OAuth1UserHandler(consumer_key=key.consumer_key, consumer_secret=key.consumer_secret)

    api = tweepy.API(auth)
    username='TheCoinMonitor_'
    tweets_list= api.user_timeline(screen_name=username, count=2)
    print (liste_id[0])
    tweet_last=tweets_list[0]
    tweet= tweets_list[1]
    if balance>195:
        if liste_id[-1]==tweet_last.id:
            print ("yeni tweet yok")

        else:
            liste_id.append(tweet_last.id)
            print(liste_id)


            price=client.futures_symbol_ticker(symbol='ETHUSDT')
            coiprice = format(float(price['price']), )
            print (coiprice)
            coiprice_int =float(coiprice)
            print (type(coiprice_int))
            quantity = (35/coiprice_int)
            price_sell= coiprice_int*1.01
            price_buy = coiprice_int*0.991
            print (price_sell)

            if coiprice_int>1000:
                price_sell_new = round (price_sell,2)
                price_buy_new = round(price_buy, 2)
            elif coiprice_int>99 and coiprice_int<1000:
                price_sell_new = round  (price_sell,3)
                price_buy_new = round (price_buy, 3)
            else:
                price_sell_new =round (price_sell,4)
                price_buy_new  =round (price_buy, 4)
            print (price_sell_new)
            print (price_buy_new)
            coipricex=round (quantity,2)
            print (coipricex)

            """
            client.futures_create_order(
                symbol='ETHUSDT',
                type='MARKET',

                workingType='MARK_PRICE',
                positionSide='LONG',
                side='BUY', # Direction ('BUY' / 'SELL'), string
                quantity=0.01, # Number of coins you wish to buy / sell, float


            )
            print ("x")
            client.futures_create_order(
                symbol='ETHUSDT',
                stopPrice=price_sell_new,
                price =price_sell_new,
                type='TAKE_PROFIT',
                closePosition=False,
                workingType='MARK_PRICE',
                positionSide='LONG',
                side='SELL', # Direction ('BUY' / 'SELL'), string
                quantity=0.01,# Number of coins you wish to buy / sell, float
            )
            """

            print(tweet.created_at)
            x=tweet.text
            m = x.split("$")
            z =m[2]
            quto = z[0:3]
            quto2 = z[4:8]
            print (quto)
            print (quto2)
            print (m)

            tele.telegram_bot(quto)
            tele.telegram_bot(quto2)
            if m[2] =='BTC SHORTED @':
                print ("xyx")
            else:
                print ("mdj")
            print(tweet.text)
            print(tweet.id)
            print(tweet.in_reply_to_screen_name)
    else:
        print ("balance 200 altında")
while True:
    signal()












