import tweepy
import key
from binance.client import Client
import pandas as pd
import send_msg as tele
import time
import  gspread




client = Client(api_key=key.Pkey, api_secret=key.Skey)
result = client.futures_account_balance(asset='USDT')  # bir listeden asset cektik

def open_order_number(symbol):

    order = client.futures_get_open_orders(symbol=symbol)

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
    x = tweet_last.text
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
            '$ETH':'ETHUSDT',
            '$SAND':'SANDUSDT',
            '$LRC':'LRCUSDT',
             '$TRX':'TRXUSDT',
            '$ALGO':'ALGOUSDT',
            '$ETC':'ETCUSDT',
            '$AVAX':'AVAXUSDT',
            '$DOT':'DOTUSDT',
            '$AR':'ARUSDT',
            '$RUNE':'RUNEUSDT',
            '$XRP':'XRPUSDT',
            '$THETA':'THETAUSDT',
            '$CRV':'CRVUSDT',
            '$ICP':'ICPUSDT',
            '$LIT ':'LITUSDT',
            '$EOS': 'EOSUSDT',
            '$GMT':'GMTUSDT',
            '$ATOM ':'ATOMUSDT'}
    dict1 = {'$SOL': 1,
             '$BTC': 0.001,
             '$COMP': 0.5,
             '$ONE': 80,
             '$ZEC': 0.25,
             '$ETH': 0.015,
             '$SAND' :25,
             '$LRC' :50,
             '$TRX':200,
             '$ALGO':80,
             '$ETC':1.5,
             '$AVAX':1,
             '$DOT':3,
             '$AR':2,
             '$RUNE':10,
             '$XRP':60,
             '$THETA':20,
             '$CRV':22,
             '$ICP':4,
             '$LIT ':40,
             '$EOS':20,
             '$GMT':21,
             '$ATOM ':2}
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

def price_sell_buy(price,buyperc,sellperc):
    coiprice = format(float(price['price']), )

    coiprice_int = float(coiprice)

    quantity = (35 / coiprice_int)
    price_sell = coiprice_int * buyperc
    price_buy = coiprice_int * sellperc


    if coiprice_int > 1000:  #sell price virgulden sonrası
        price_sell_new = round(price_sell, 0)
        price_buy_new = round(price_buy, 0)
    elif coiprice_int > 99 and coiprice_int < 1000:
        price_sell_new = round(price_sell, 2)
        price_buy_new = round(price_buy, 2)
    elif coiprice_int >0.1 and coiprice_int <99:
        price_sell_new = round(price_sell, 3)
        price_buy_new = round(price_buy, 3)
    else:
        price_sell_new = round(price_sell, 4)
        price_buy_new = round(price_buy, 4)

    coipricex = round(quantity, 2)

    return [price_sell_new,price_buy_new]

def long_position (symbol,quantity,price_sell_new):
    client.futures_create_order(
        symbol=symbol,
        type='MARKET',
        recvWindow=25000,
        workingType='MARK_PRICE',
        positionSide='LONG',
        side='BUY',  # Direction ('BUY' / 'SELL'), string
        quantity=quantity,  # Number of coins you wish to buy / sell, float

    )
    time.sleep(1)
    client.futures_create_order(
        symbol=symbol,
        stopPrice=price_sell_new,
        price=price_sell_new,
        type='TAKE_PROFIT',
        recvWindow=25000,
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
        recvWindow=25000,
        workingType='MARK_PRICE',
        positionSide='SHORT',
        side='SELL',  # Direction ('BUY' / 'SELL'), string
        quantity=quantity,  # Number of coins you wish to buy / sell, float

    )
    time.sleep(1)
    client.futures_create_order(
        symbol=symbol,
        stopPrice=price_sell_new,
        price=price_sell_new,
        recvWindow=25000,
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
        tele.telegram_bot("server online11")

def sheets_add(balance):
    gc =gspread.service_account(filename='credentials.json')

    sh = gc.open_by_key('15IDisjoICpEu6t2ByuRmsjwK8KyEFOuTCCPMgbt1oxo')
    worksheet =sh.sheet1
    res2= worksheet.get('A2')
    res1=res2[0]
    res_str=res1[0]
    res =int(res_str)

    worksheet.update_cell(6,2,balance)

    return(res)








