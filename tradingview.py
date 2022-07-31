import pandas as pd
import ccxt, config

import time
import send_msg as tele

import functions as func

from binance.client import Client
import firebase_admin
from firebase_admin import credentials, firestore
from tradingview_ta import TA_Handler, Interval, Exchange
import calendar
import key
from datetime import datetime

longgiris = 0
shortgiris = 0
sayici_giris_control = 0
sheetsymbolx = 0
sheetssymboly = 0
macdlast = 0
engulfing = 0
buysignallast = 0
sellsignallast = 0
coipricefloat = 0
sellsignallast1 = 0
sellsignallast2 = 0
str_sellsignallast1 = 0
str_sellsignallast2 = 0
kimlik = credentials.Certificate("ema_class.json")

app = firebase_admin.initialize_app(kimlik)


class Macdema():

    def __init__(self, symbol, timeframe, quantity, buyvalue, sellvalue):
        self.symbol = symbol
        self.longgiris = longgiris
        self.shortgiris = shortgiris
        self.timeframe = timeframe
        self.sayici_giris_control = sayici_giris_control
        self.quantity = quantity
        self.buyvalue = buyvalue
        self.sellvalue = sellvalue
        self.buysignallast = buysignallast
        self.sellsignallast = sellsignallast
        self.sellsignallast1 = sellsignallast1
        self.sellsignallast2 = sellsignallast2
        self.str_sellsignallast1 = str_sellsignallast1
        self.str_sellsignallast2 = str_sellsignallast2

        self.coipricefloat = coipricefloat

    def dfall(self, symbol, timeframe):

        exchange = ccxt.binance({
            "apiKey": config.apiKey,
            "secret": config.secretKey,

            'options': {
                'defaultType': 'future'
            },
            'enableRateLimit': True,
            'adjustForTimeDifference': True
        })
        order_approve = func.open_order_number(self.symbol)

        try:
            if self.shortgiris == 1 or self.longgiris == 1 or order_approve == 0:  # alıs satıstan sonra 100 cycledan sonra tekrar işleme açma
                self.sayici_giris_control += 1
                if self.sayici_giris_control == 10:
                    print(symbol, timeframe, self.sayici_giris_control)
                    self.longgiris = 0
                    self.shortgiris = 0
                    self.sellsignallast = 0
                    self.buysignallast = 0

                    self.sayici_giris_control = 0


            else:
                handler = TA_Handler(
                    symbol=symbol,
                    exchange="BINANCE",
                    screener="crypto",
                    interval=timeframe,
                    timeout=None,
                    proxies={'http': '47.242.84.173:3128', 'http': '181.205.20.195:999', 'http': '192.111.135.17:18302',
                             'http': '103.108.228.185:7497'}
                )

                analysis = handler.get_analysis().summary

                analysis_str = str(analysis)

                symbolrec = analysis['RECOMMENDATION']

                dt = time.gmtime()
                ts = calendar.timegm(dt)
                ts_str = str(ts)

                x = self.symbol + self.timeframe + ts_str

                db = firestore.client()  # db e baglantı

                document = db.collection(self.symbol + self.timeframe).document(x)
                docId = document.id
                document.set({
                    "id": ts_str,

                    "position": symbolrec,

                })

                list1 = []
                list2 = []

                snapshots = list(db.collection(self.symbol + self.timeframe).get())
                df = pd.DataFrame()
                for snap in snapshots:
                    X = snap.to_dict()
                    key = ['position']
                    m = ([snap.get(k) for k in key])

                    key2 = ['id']
                    n = ([snap.get(k) for k in key2])
                    list1.append(m)
                    list2.append(n)

                print(list1)
                print(list2)
                d = {'situation': list1, 'time': list2}
                print(d)
                df = pd.DataFrame(d, columns=['situation', 'time'])
                print(df)
                sellsignal = df.iloc[:, 0]  # bununla data set içindeki 1. kolonu cekiyorum
                self.sellsignallast1 = (sellsignal.iloc[-1])
                self.sellsignallast2 = (sellsignal.iloc[-2])
                print(self.sellsignallast2)
                print(self.sellsignallast1)
                print(type(sellsignallast1))
                print(type(sellsignallast2))
                self.str_sellsignallast1 = str(self.sellsignallast1)
                self.str_sellsignallast2 = str(self.sellsignallast2)
                print(type(self.str_sellsignallast1))
                print(type(self.str_sellsignallast2))

                if self.str_sellsignallast2 != self.str_sellsignallast1:
                    print("esit_degil")
                    if self.str_sellsignallast1 == "['BUY']" and self.str_sellsignallast2 == "['SELL']" or self.str_sellsignallast2 == "['STRONG_SELL']" or self.str_sellsignallast2 == "['NEUTRAL']":
                        self.buysignallast = 1

                    elif self.str_sellsignallast1 == "['SELL']" and self.str_sellsignallast2 == "['BUY']" or self.str_sellsignallast2 == "['STRONG_BUY']" or self.str_sellsignallast2 == "['NEUTRAL']":
                        self.sellsignallast = 1

                    elif self.str_sellsignallast1 == "['STRONG_SELL']":
                        self.sellsignallast = 1

                    elif self.str_sellsignallast1 == "['STRONG_BUY']":
                        self.buysignallast = 1


                    elif self.str_sellsignallast1 == "['NEUTRAL']" and self.str_sellsignallast2 == "['SELL']" or self.str_sellsignallast2 == "['STRONG_SELL']":
                        self.buysignallast = 1

                    elif self.str_sellsignallast1 == "['NEUTRAL']" and self.str_sellsignallast2 == "['BUY']" or self.str_sellsignallast2 == "['STRONG_BUY']":
                        self.sellsignallast = 1
                print(self.sellsignallast)
                print(self.buysignallast)

                try:

                    client = Client(api_key="YYchbhcI9jMSOIyTIFwHwJD2iEh71q4wH9RXZixtWU1UurBqFTgawLt2zkcTJm1T",
                                    api_secret="E7vdV4JPaMtqbQGGozkSBNWeB5xPcDJSSD8AdqhHqPa0Ep6yQvbL8yYbtvWmPn4B")
                    result = client.futures_account_balance(asset='USDT',
                                                            recvWindow=49000)  # bir listeden asset cektik
                    balance = float(result[6]['withdrawAvailable'])

                    price = client.futures_symbol_ticker(symbol=self.symbol, recvWindow=45000)

                    tp_price = func.price_sell_buy(price, self.buyvalue, self.sellvalue)
                    price_sell_new = tp_price[0]
                    price_buy_new = tp_price[1]
                    print(price_buy_new)
                    print(price_sell_new)
                    order_approve = func.open_order_number(self.symbol)
                    print("order approve", order_approve)
                    print("quantity", self.quantity)

                    if self.buysignallast == 1 or self.sellsignallast == 1:
                        if order_approve == 1:

                            if balance > 200:
                                try:
                                    if self.buysignallast == 1:
                                        print('long gir')
                                        tele.telegram_bot('long gir-tradingview')
                                        tele.telegram_bot(symbol)
                                        self.longgiris += 1
                                        func.long_position(self.symbol, self.quantity,
                                                           price_sell_new)  # alıs olusturma fonk

                                        time.sleep(30)
                                    elif self.sellsignallast == 1:
                                        print("short_gir")

                                        tele.telegram_bot("short_gir-tradingview")
                                        tele.telegram_bot(symbol)
                                        self.shortgiris += 1
                                        func.short_position(self.symbol, self.quantity,
                                                            price_buy_new)  # satıs olusturma fonk
                                except:
                                    tele.telegram_bot('fiyat alamadı1')



                        else:
                            islemfazla = "islem sayisi 5 den fazlastrtegy2" + " " + self.symbol + " " + self.timeframe
                            tele.telegram_bot(islemfazla)
                    else:
                        print("setup olusmadi")

                except:
                    tele.telegram_bot('fiyat alamadı2')
        except ccxt.BaseError as Error:
            print("[ERROR] ", Error)


coin2 = Macdema('API3USDT', "1h", 15, 1.007, 0.993)
coin1 = Macdema('WOOUSDT', "1h", 100, 1.007, 0.993)
coin3 = Macdema('CELOUSDT', "1h", 30, 1.007, 0.993)
coin4 = Macdema('ARPAUSDT', "1h", 600, 1.007, 0.993)
coin5 = Macdema('LPTUSDT', "1h", 3, 1.007, 0.993)

coin7 = Macdema('OMGUSDT', "1h", 15, 1.007, 0.993)
coin8 = Macdema('OPUSDT', "1h", 40, 1.007, 0.993)
coin9 = Macdema('UNFIUSDT', "1h", 6, 1.007, 0.993)
coin10 = Macdema('PEOPLEUSDT', "1h", 100, 1.007, 0.993)


coin2a = Macdema('API3USDT', "2h", 15, 1.007, 0.993)
coin1a = Macdema('WOOUSDT', "2h", 100, 1.007, 0.993)
coin3a = Macdema('CELOUSDT', "2h", 30, 1.007, 0.993)
coin4a = Macdema('ARPAUSDT', "2h", 600, 1.007, 0.993)
coin5a = Macdema('LPTUSDT', "2h", 3, 1.007, 0.993)

coin7a = Macdema('OMGUSDT', "2h", 15, 1.007, 0.993)
coin8a = Macdema('OPUSDT', "2h", 40, 1.007, 0.993)
coin9a = Macdema('UNFIUSDT', "2h", 6, 1.007, 0.993)
coin10a = Macdema('PEOPLEUSDT', "2h", 100, 1.007, 0.993)


while True:
    coin2.dfall('API3USDT', "1h")
    time.sleep(30)
    coin1.dfall('WOOUSDT', "1h")
    time.sleep(30)
    coin3.dfall('CELOUSDT', "1h")
    time.sleep(30)
    coin4.dfall('ARPAUSDT', "1h")
    time.sleep(30)
    coin5.dfall('LPTUSDT', "1h")
    time.sleep(30)

    coin7.dfall('OMGUSDT', "1h")
    time.sleep(30)
    coin8.dfall('OPUSDT', "1h")
    time.sleep(30)
    coin9.dfall('UNFIUSDT', "1h")
    time.sleep(30)
    coin10.dfall('PEOPLEUSDT', "1h")
    time.sleep(30)


    coin2a.dfall('API3USDT', "2h")
    time.sleep(30)
    coin1a.dfall('WOOUSDT', "2h")
    time.sleep(30)
    coin3a.dfall('CELOUSDT', "2h")
    time.sleep(30)
    coin4a.dfall('ARPAUSDT', "2h")
    time.sleep(30)
    coin5a.dfall('LPTUSDT', "2h")
    time.sleep(30)

    coin7a.dfall('OMGUSDT', "2h")
    time.sleep(30)
    coin8a.dfall('OPUSDT', "2h")
    time.sleep(30)
    coin9a.dfall('UNFIUSDT', "2h")
    time.sleep(30)
    coin10a.dfall('PEOPLEUSDT', "2h")


    time.sleep(900)
