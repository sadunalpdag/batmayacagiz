

from binance.client import Client


import functions as func
import time

import key
import send_msg as tele
import schedule
import time
liste_id=['0']
sayici = 0

def signal():
    global price_sell_new
    func.server_online() #server her bir saate telegram messaj









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
    print ("quantity",quantity)





    #fonksiyonlardan sembol cekme
    print("symbol",symbol_func)
    if balance>200:
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

            order_approve=func.open_order_number(symbol_func)
            print ("order approve",order_approve)
            """"
            if order_approve==1:
                try:
                    if position_direct =='LONGED':
                        func.long_position (symbol_func,quantity,price_sell_new)
                    else:
                        func.short_position (symbol_func,quantity,price_buy_new)
                except:
                    tele.telegram_bot('hata_oldu_devam')
            else:
                tele.telegram_bot("islem sayisi 5 den fazla")
                """









            print(tweet.text)
            print(tweet.id)
            print(tweet.in_reply_to_screen_name)
    else:
        print ("balance 200 altında")
        tele.telegram_bot("balance 200 altında")

schedule.every(15).seconds.do(signal)
while True:
    schedule.run_pending()
if __name__ == "main":
        signal()