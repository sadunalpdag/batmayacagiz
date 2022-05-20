import tweepy
import key
from binance.client import Client
import pandas as pd
import send_msg as tele
import time
import schedule



client = Client(api_key=key.Pkey, api_secret=key.Skey)
result = client.futures_account_balance(asset='USDT')  # bir listeden asset cektik

def open_order_number(symbol):

    order = client.futures_get_open_orders(symbol=symbol)
    print (order)
    if (len(order))==0:
        order_give=1
    else:
        m = pd.DataFrame.from_dict(order)


        l = len(m[m.origType == 'TAKE_PROFIT'])
        if l>=5:
            order_give=0
        else:
            order_give=1
    return (order_give)



def tweet_data(member_name):
    auth = tweepy.OAuth1UserHandler(consumer_key=key.consumer_key, consumer_secret=key.consumer_secret)
    api = tweepy.API(auth)
    username = member_name
    tweets_list = api.user_timeline(screen_name=username, count=2)
    tweet_last = tweets_list[0]
    tweet = tweets_list[1]
    x = tweet.text
    n = x.split()
    print(n)
    symbol_tweet = n[1]
    position_side = n[2]
    return [tweet_last,tweet,symbol_tweet,position_side]

def checkKey(key):
    dict = {'$SOL': 'SOLUSDT',
            '$BTC': 'BTCUSDT',
            '$COMP': 'COMPUSDT',
            '$ONE':'ONEUSDT',
            '$ZEC':'ZECUSDT',
            '$ETH ':'ETHUSDT',
            '$SAND':'SANDUSDT',
            '$LRC':'LRCUSDT',
            '$SOL':'SOLUSDT',
            '$TRX':'TRXUSDT',
            '$ALGO':'ALGOUSDT',
            '$ETC':'ETCUSDT',
            '$AVAX':'AVAXUSDT',
            '$DOT':'DOTUSDT',
            '$AR':'ARUSDT',
            '$RUNE':'RUNEUSDT'}
    dict1 = {'$SOL': 1,
             '$BTC': 0.001,
             '$COMP': 0.5,
             '$ONE': 80,
             '$ZEC': 0.25,
             '$ETH ': 0.015,
             '$SAND' :25,
             '$LRC' :50,
             '$SOL':1,
             '$TRX':200,
             '$ALGO':80,
             '$ETC':1.5,
             '$AVAX':1,
             '$DOT':3,
             '$AR':2,
             '$RUNE':10}
    if key in dict.keys():
        #print("Present, ", end=" ")
        #print("value =", dict[key])
        symbol_come_func =dict[key]
        quantity =dict1[key]
        print(quantity)
    else:
        symbol_come_func = 0
        quantity=0
        print ("no symbol")
    return [symbol_come_func,quantity]

def price_sell_buy(price):
    coiprice = format(float(price['price']), )

    coiprice_int = float(coiprice)

    quantity = (35 / coiprice_int)
    price_sell = coiprice_int * 1.01
    price_buy = coiprice_int * 0.991


    if coiprice_int > 1000:
        price_sell_new = round(price_sell, 0)
        price_buy_new = round(price_buy, 0)
    elif coiprice_int > 99 and coiprice_int < 1000:
        price_sell_new = round(price_sell, 3)
        price_buy_new = round(price_buy, 3)
    else:
        price_sell_new = round(price_sell, 4)
        price_buy_new = round(price_buy, 4)

    coipricex = round(quantity, 2)
    print(coipricex)
    return [price_sell_new,price_buy_new]

def long_position (symbol,quantity,price_sell_new):
    client.futures_create_order(
        symbol=symbol,
        type='MARKET',

        workingType='MARK_PRICE',
        positionSide='LONG',
        side='BUY',  # Direction ('BUY' / 'SELL'), string
        quantity=quantity,  # Number of coins you wish to buy / sell, float

    )

    client.futures_create_order(
        symbol=symbol,
        stopPrice=price_sell_new,
        price=price_sell_new,
        type='TAKE_PROFIT',
        closePosition=False,
        workingType='MARK_PRICE',
        positionSide='LONG',
        side='SELL',  # Direction ('BUY' / 'SELL'), string
        quantity=quantity,
    )

def short_position (symbol,quantity,price_sell_new):

    client.futures_create_order(
        symbol=symbol,
        type='MARKET',

        workingType='MARK_PRICE',
        positionSide='SHORT',
        side='SELL',  # Direction ('BUY' / 'SELL'), string
        quantity=quantity,  # Number of coins you wish to buy / sell, float

    )

    client.futures_create_order(
        symbol=symbol,
        stopPrice=price_sell_new,
        price=price_sell_new,
        type='TAKE_PROFIT',
        closePosition=False,
        workingType='MARK_PRICE',
        positionSide='SHORT',
        side='BUY',  # Direction ('BUY' / 'SELL'), string
        quantity=quantity,
    )
sayici = 0
def server_online():
    global sayici


    sayici += 1
    print("sayici", sayici)
    if sayici == 120:
        sayici = 0
        tele.telegram_bot("server online")










