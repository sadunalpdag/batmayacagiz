

import tweepy

from binance.client import Client


import functions as func
import time

import key
import send_msg as tele

liste_id=['0']



def signal():
    global price_sell_new

    time.sleep(60)
    client = Client(api_key=key.Pkey, api_secret=key.Skey)
    result = client.futures_account_balance(asset='USDT') # bir listeden asset cektik
    balance = float(result[6]['withdrawAvailable']) #with drawal codu ile aldık
    #print (balance)




    tweet_data_info = func.tweet_data('TheCoinMonitor_')  # fonksiyonlardan sembol cekme
    tweet_last=tweet_data_info[0]
    tweet=tweet_data_info[1]
    symbol_tweet=tweet_data_info[2]
    position_direct = tweet_data_info[3]

    key_def = func.checkKey(symbol_tweet)
    symbol_func=key_def[0]
    quantity =key_def[1]
    print (quantity)
    #fonksiyonlardan sembol cekme
    print(symbol_func)
    if balance>195:
        if liste_id[-1]==tweet_last.id or symbol_func==0:
            print ("yeni tweet yok")

        else:
            liste_id.append(tweet_last.id)
            print(liste_id)
            tele.telegram_bot(symbol_tweet)
            tele.telegram_bot(position_direct)
            tele.telegram_bot(balance)








            price=client.futures_symbol_ticker(symbol=symbol_func)
            tp_price=func.price_sell_buy(price)
            price_sell_new=tp_price[0]
            price_buy_new=tp_price[1]

            print(price_buy_new)
            print(price_sell_new)
            if position_direct =='LONGED':
                func.long_position (symbol_func,quantity,price_sell_new)
            else:
                func.short_position (symbol_func,quantity,price_buy_new)
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



            tele.telegram_bot(symbol_tweet)
            tele.telegram_bot(position_direct)


            print(tweet.text)
            print(tweet.id)
            print(tweet.in_reply_to_screen_name)
    else:
        print ("balance 200 altında")
        tele.telegram_bot("balance 200 altında")
while True:
    signal()












