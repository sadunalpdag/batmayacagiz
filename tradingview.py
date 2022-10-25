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
        try:
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
        except:
            tele.telegram_bot('fiyat alamadıtrading_cctx')

        try:
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
            print(self.symbol)
            print(symbolrec)
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
                    if self.str_sellsignallast1 == "['BUY']" and self.str_sellsignallast2 != "['STRONG_BUY']" :
                        self.buysignallast = 1
                        print ("x")
                    elif self.str_sellsignallast1 == "['BUY']" and self.str_sellsignallast2 == "['STRONG_BUY']" :
                         self.sellsignallast = 1
                         print ("x")



                    elif self.str_sellsignallast1 == "['SELL']" and self.str_sellsignallast2 != "['STRONG_SELL']" :
                        self.sellsignallast = 1
                        print ("y")

                    elif self.str_sellsignallast1 == "['SELL']" and self.str_sellsignallast2 == "['STRONG_SELL']" :
                        self.buysignallast = 1
                        print ("y")

                    elif self.str_sellsignallast1 == "['STRONG_SELL']":
                        self.sellsignallast = 1
                        print("e")

                    elif self.str_sellsignallast1 == "['STRONG_BUY']":
                        self.buysignallast = 1
                        print("z")


                    elif self.str_sellsignallast1 == "['NEUTRAL']" and self.str_sellsignallast2 == "['SELL']" :
                        self.buysignallast = 1
                        print("b")
                    elif self.str_sellsignallast1 == "['NEUTRAL']" and self.str_sellsignallast2 == "['STRONG_SELL']":
                        self.buysignallast = 1
                        print("b")

                    elif self.str_sellsignallast1 == "['NEUTRAL']" and self.str_sellsignallast2 == "['BUY']":
                        self.sellsignallast = 1
                        print("m")
                    elif self.str_sellsignallast1 == "['NEUTRAL']" and self.str_sellsignallast2 == "['STRONG_BUY']":
                        self.sellsignallast = 1
                        print("m")
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
                                        tele.telegram_bot(self.str_sellsignallast1 + self.str_sellsignallast2)
                                        tele.telegram_bot(self.buysignallast)
                                        tele.telegram_bot(self.sellsignallast)
                                        tele.telegram_bot(symbol)
                                        self.longgiris += 1
                                        self.buysignallast = 0
                                        func.long_position(self.symbol, self.quantity,
                                                           price_sell_new)  # alıs olusturma fonk

                                        time.sleep(30)
                                    elif self.sellsignallast == 1:
                                        print("short_gir")

                                        tele.telegram_bot("short_gir-tradingview")
                                        tele.telegram_bot(self.str_sellsignallast1 + self.str_sellsignallast2)
                                        tele.telegram_bot(self.buysignallast)
                                        tele.telegram_bot(self.sellsignallast)
                                        tele.telegram_bot(symbol)
                                        self.shortgiris += 1
                                        self.sellsignallast = 0
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


coin2 = Macdema('API3USDT', "1h", 33, 1.006, 0.994)
coin1 = Macdema('WOOUSDT', "1h", 220, 1.006, 0.994)
coin3 = Macdema('CELOUSDT', "1h", 60, 1.006, 0.994)
coin4 = Macdema('ARPAUSDT', "1h", 1200, 1.006, 0.994)
coin5 = Macdema('LPTUSDT', "1h", 11, 1.006, 0.994)

coin7 = Macdema('OMGUSDT', "1h", 33, 1.006, 0.994)
coin8 = Macdema('OPUSDT', "1h", 88, 1.006, 0.994)
coin9 = Macdema('UNFIUSDT', "1h", 19 ,1.006, 0.994)
coin11 = Macdema('ARUSDT', "1h", 8, 1.006, 0.994)
coin12 = Macdema('DOTUSDT', "1h", 9, 1.006, 0.994)
coin13 = Macdema('ETCUSDT', "1h", 4, 1.006, 0.994)
coin14 = Macdema('ALGOUSDT', "1h", 160, 1.006, 0.994)
coin15 = Macdema('TRXUSDT', "1h", 380, 1.006, 0.994)
coin16 = Macdema('LRCUSDT', "1h", 90, 1.006, 0.994)
coin17 = Macdema('SANDUSDT', "1h", 50, 1.006, 0.994)
coin18 = Macdema('YFIUSDT', "1h", 0.008, 1.006, 0.994)

coin20 = Macdema('SUSHIUSDT', "1h", 50, 1.006, 0.994)
coin21 = Macdema('NEARUSDT', "1h", 19, 1.006, 0.994)
coin22 = Macdema('MATICUSDT', "1h", 60, 1.006, 0.994)
coin23 = Macdema('BELUSDT', "1h", 55, 1.006, 0.994)
coin24 = Macdema('BLZUSDT', "1h", 310, 1.006, 0.994)
coin25 = Macdema('KAVAUSDT', "1h", 30, 1.006, 0.994)
coin26 = Macdema('CHZUSDT', "1h", 390, 1.006, 0.994)
coin31 = Macdema('QTUMUSDT', "1h", 23, 1.006, 0.994)
coin32 = Macdema('CHRUSDT', "1h", 275, 1.006, 0.994)
coin33 = Macdema('OCEANUSDT', "1h", 178, 1.006, 0.994)
coin34 = Macdema('ALPHAUSDT', "1h", 310, 1.006, 0.994)
coin35 = Macdema('XRPUSDT', "1h", 145, 1.006, 0.994)
coin36 = Macdema('BNBUSDT', "1h", 0.16, 1.006, 0.994)
coin37 = Macdema('ATOMUSDT', "1h", 7, 1.006, 0.994)





coin2a = Macdema('API3USDT', "2h", 50, 1.007, 0.993)
coin1a = Macdema('WOOUSDT', "2h", 320, 1.007, 0.993)
coin3a = Macdema('CELOUSDT', "2h", 100, 1.007, 0.993)
coin4a = Macdema('ARPAUSDT', "2h", 1450, 1.007, 0.993)
coin5a = Macdema('LPTUSDT', "2h", 11, 1.007, 0.993)

coin7a = Macdema('OMGUSDT', "2h", 42, 1.007, 0.993)
coin8a = Macdema('OPUSDT', "2h", 120, 1.007, 0.993)
coin9a = Macdema('UNFIUSDT', "2h", 20, 1.007, 0.993)
coin11a = Macdema('ARUSDT', "2h", 9, 1.007, 0.993)
coin12a = Macdema('DOTUSDT', "2h", 10, 1.007, 0.993)
coin13a = Macdema('ETCUSDT', "2h", 4, 1.007, 0.993)
coin14a = Macdema('ALGOUSDT', "2h", 240, 1.007, 0.993)
coin15a = Macdema('TRXUSDT', "2h", 510, 1.007, 0.993)
coin16a = Macdema('LRCUSDT', "2h", 165, 1.007, 0.993)
coin17a = Macdema('SANDUSDT', "2h", 62, 1.007, 0.993)
coin18a = Macdema('YFIUSDT', "2h", 0.008, 1.007, 0.993)

coin20a = Macdema('SUSHIUSDT', "2h", 46, 1.007, 0.993)
coin21a = Macdema('NEARUSDT', "2h", 22, 1.007, 0.993)
coin22a = Macdema('MATICUSDT', "2h", 80, 1.006, 0.994)
coin23a = Macdema('BELUSDT', "2h", 60, 1.006, 0.994)
coin24a = Macdema('BLZUSDT', "2h", 330, 1.006, 0.994)
coin25a = Macdema('KAVAUSDT', "2h", 33, 1.006, 0.994)
coin26a = Macdema('CHZUSDT', "2h", 444, 1.006, 0.994)
coin31a = Macdema('QTUMUSDT', "2h", 33, 1.006, 0.994)
coin32a = Macdema('CHRUSDT', "2h", 310, 1.006, 0.994)
coin33a = Macdema('OCEANUSDT', "2h", 244, 1.006, 0.994)
coin34a = Macdema('ALPHAUSDT', "2h", 400, 1.006, 0.994)
coin35a = Macdema('XRPUSDT', "2h", 154, 1.006, 0.994)
coin36a =  Macdema('BNBUSDT', "2h", 0.16, 1.006, 0.994)
coin37a = Macdema('ATOMUSDT', "2h", 6, 1.006, 0.994)




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
    coin11.dfall('ARUSDT', "1h")
    time.sleep(30)
    coin12.dfall('DOTUSDT', "1h")
    time.sleep(30)
    coin13.dfall('ETCUSDT', "1h")
    time.sleep(30)
    coin14.dfall('ALGOUSDT', "1h")
    time.sleep(30)
    coin15.dfall('TRXUSDT', "1h")
    time.sleep(30)
    coin16.dfall('LRCUSDT', "1h")
    time.sleep(30)
    coin17.dfall('SANDUSDT', "1h")
    time.sleep(30)
    coin18.dfall('YFIUSDT', "1h")
    time.sleep(30)



    coin20.dfall('SUSHIUSDT', "1h")
    time.sleep(30)
    coin21.dfall('NEARUSDT', "1h")
    time.sleep(30)
    coin22.dfall('MATICUSDT', "1h")
    time.sleep(30)
    coin23.dfall('BELUSDT', "1h")
    time.sleep(30)
    coin24.dfall('BLZUSDT', "1h")
    time.sleep(30)
    coin25.dfall('KAVAUSDT', "1h")
    time.sleep(30)
    coin26.dfall('CHZUSDT', "1h")
    time.sleep(30)
    coin31.dfall('QTUMUSDT', "1h")
    time.sleep(30)
    coin32.dfall('CHRUSDT', "1h")
    time.sleep(30)
    coin33.dfall('OCEANUSDT', "1h")
    time.sleep(30)
    coin34.dfall('ALPHAUSDT', "1h")
    time.sleep(30)
    coin35.dfall('XRPUSDT', "1h")
    time.sleep(30)
    coin36.dfall('BNBUSDT', "1h")
    time.sleep(30)
    coin37.dfall('ATOMUSDT', "1h")
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
    coin11a.dfall('ARUSDT', "2h")
    time.sleep(30)
    coin12a.dfall('DOTUSDT', "2h")
    time.sleep(30)
    coin13a.dfall('ETCUSDT', "2h")
    time.sleep(30)
    coin14a.dfall('ALGOUSDT', "2h")
    time.sleep(30)
    coin15a.dfall('TRXUSDT', "2h")
    time.sleep(30)
    coin16a.dfall('LRCUSDT', "2h")
    time.sleep(30)
    coin17a.dfall('SANDUSDT', "2h")
    time.sleep(30)


    coin18a.dfall('YFIUSDT', "2h")
    time.sleep(30)



    coin20a.dfall('SUSHIUSDT', "2h")
    time.sleep(30)
    coin21a.dfall('NEARUSDT', "2h")
    time.sleep(30)
    coin22a.dfall('MATICUSDT', "2h")
    time.sleep(30)
    coin23a.dfall('BELUSDT', "2h")
    time.sleep(30)
    coin24a.dfall('BLZUSDT', "2h")
    time.sleep(30)
    coin25a.dfall('KAVAUSDT', "2h")
    time.sleep(30)
    coin26a.dfall('CHZUSDT', "2h")
    time.sleep(30)
    coin31a.dfall('QTUMUSDT', "2h")
    time.sleep(30)
    coin32a.dfall('CHRUSDT', "2h")
    time.sleep(30)
    coin33a.dfall('OCEANUSDT', "2h")
    time.sleep(30)
    coin34a.dfall('ALPHAUSDT', "2h")
    time.sleep(30)
    coin35a.dfall('XRPUSDT', "2h")
    time.sleep(30)
    coin36a.dfall('BNBUSDT', "2h")
    time.sleep(30)
    coin37a.dfall('ATOMUSDT', "2h")
    time.sleep(30)


    time.sleep(400)
