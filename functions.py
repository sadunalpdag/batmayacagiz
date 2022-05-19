import tweepy
import key



def tweet_data(member_name):
    auth = tweepy.OAuth1UserHandler(consumer_key=key.consumer_key, consumer_secret=key.consumer_secret)
    api = tweepy.API(auth)
    username = member_name
    tweets_list = api.user_timeline(screen_name=username, count=2)
    tweet_last = tweets_list[0]
    tweet = tweets_list[1]
    x = tweet.text
    n = x.split()
    #print(n)
    symbol_tweet = n[1]
    position_side = n[2]
    return [tweet_last,tweet,symbol_tweet,position_side]


def checkKey(key):
    dict = {'$SOL': 'SOLUSDT', '$BTC': 'BTCUSDT', '$COMP': 'COMPUSDT','$ONE':'ONEUSDT','$ZEC':'ZECUSDT','$ETH ':'ETHUSDT'}
    if key in dict.keys():
        #print("Present, ", end=" ")
        #print("value =", dict[key])
        symbol_come_func =dict[key]
    else:
        symbol_come_func = 0
    return (symbol_come_func)

def price_sell_buy(price):
    coiprice = format(float(price['price']), )

    coiprice_int = float(coiprice)

    quantity = (35 / coiprice_int)
    price_sell = coiprice_int * 1.01
    price_buy = coiprice_int * 0.991


    if coiprice_int > 1000:
        price_sell_new = round(price_sell, 2)
        price_buy_new = round(price_buy, 2)
    elif coiprice_int > 99 and coiprice_int < 1000:
        price_sell_new = round(price_sell, 3)
        price_buy_new = round(price_buy, 3)
    else:
        price_sell_new = round(price_sell, 4)
        price_buy_new = round(price_buy, 4)

    coipricex = round(quantity, 2)
    print(coipricex)
    return [price_sell_new,price_buy_new]





















def long(symbol,price_sell_new,quantity):
    client.futures_create_order(
        symbol=symbol,
        type='MARKET',

        workingType='MARK_PRICE',
        positionSide='LONG',
        side='BUY',  # Direction ('BUY' / 'SELL'), string
        quantity=0.01,  # Number of coins you wish to buy / sell, float

    )
    print("x")
    client.futures_create_order(
        symbol='ETHUSDT',
        stopPrice=price_sell_new,
        price=price_sell_new,
        type='TAKE_PROFIT',
        closePosition=False,
        workingType='MARK_PRICE',
        positionSide='LONG',
        side='SELL',  # Direction ('BUY' / 'SELL'), string
        quantity=quantity,  # Number of coins you wish to buy / sell, float
    )
