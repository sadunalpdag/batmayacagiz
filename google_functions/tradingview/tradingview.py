from tradingview_ta import TA_Handler, Interval, Exchange

import time
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import calendar

kimlik = credentials.Certificate("ema_class.json")

app = firebase_admin.initialize_app(kimlik)
kesisimmacdsayac = 0
kesisimmovaverage = 0
longgiris = 0
shortgiris = 0
sayici_giris_control = 0
sheetsymbolx = 0
sheetssymboly = 0
macdlast = 0
slowmacd = 0
fastmacd =0
class Macdema():

    def __init__(self, symbol, timeframe, quantity, buyvalue, sellvalue):
        self.symbol = symbol
        self.kesisimmacdsayac = kesisimmacdsayac
        self.longgiris = longgiris
        self.shortgiris = shortgiris
        self.timeframe = timeframe
        self.sayici_giris_control = sayici_giris_control
        self.macdlast = macdlast
        self.slowmacd=slowmacd
        self.fastmacd=fastmacd
        self.quantity = quantity
        self.buyvalue = buyvalue
        self.sellvalue = sellvalue



    def dfall(self, symbol, timeframe):


        handler = TA_Handler(
            symbol=symbol,
            exchange="BINANCE",
            screener="crypto",
            interval=timeframe,
            timeout=None,
            proxies = {'http': '47.242.84.173:3128', 'http': '181.205.20.195:999','http': '192.111.135.17:18302' ,'http': '103.108.228.185:7497'}
        )

        analysis = handler.get_analysis().summary

        analysis_str =str(analysis)
        print (symbol + analysis_str)
        self.symbolrec=analysis['RECOMMENDATION']
        print (self.symbolrec)
        dt = time.gmtime()
        ts = calendar.timegm(dt)
        ts_str =str(ts)

        x=self.symbol+self.timeframe+ts_str

        db = firestore.client()  # db e baglantı

        document = db.collection(self.symbol).document(x)
        docId = document.id
        document.set({
            "id": ts_str,

            "position": self.symbolrec,


        })

coin2 = Macdema('ETHUSDT', "1d", 0.015, 1.02, 0.98)
coin1 = Macdema('BTCUSDT', "1d", 0.001, 1.02, 0.98)
coin3 = Macdema('ATOMUSDT', "1d", 2, 1.02, 0.98)
coin4 = Macdema('EOSUSDT', "1d", 20, 1.02, 0.98)
coin5 = Macdema('LITUSDT', "1d", 40, 1.02, 0.98)
coin6 = Macdema('BNBUSDT', "1d", 0.1, 1.02, 0.98)

coin7 = Macdema('CRVUSDT', "1d", 22, 1.02, 0.98)
coin8 = Macdema('THETAUSDT', "1d", 20, 1.02, 0.98)
coin9 = Macdema('XRPUSDT', "1d", 60, 1.02, 0.98)
coin10 = Macdema('RUNEUSDT', "1d", 10, 1.02, 0.98)
coin11 = Macdema('ARUSDT', "1d", 2, 1.02, 0.98)
coin12 = Macdema('DOTUSDT', "1d", 3, 1.02, 0.98)
coin13 = Macdema('ETCUSDT', "1d", 1.5, 1.02, 0.98)
coin14 = Macdema('ALGOUSDT', "1d", 80, 1.02, 0.98)
coin15 = Macdema('TRXUSDT', "1d", 200, 1.02, 0.98)
coin16 = Macdema('LRCUSDT', "1d", 50, 1.02, 0.98)
coin17 = Macdema('SANDUSDT', "1d", 25, 1.02, 0.98)
coin18 = Macdema('AVAXUSDT', "1d", 1, 1.02, 0.98)
coin19 = Macdema('COTIUSDT', "1d", 220, 1.02, 0.98)
coin20 = Macdema('LINKUSDT', "1d", 4, 1.02, 0.98)
coin21 = Macdema('NEARUSDT', "1d", 9, 1.02, 0.98)

coin24 = Macdema('MATICUSDT', "1d", 40, 1.02, 0.98)
coin25 = Macdema('BELUSDT', "1d", 30, 1.02, 0.98)
coin26 = Macdema('KNCUSDT', "1d", 20, 1.02, 0.98)
coin27 = Macdema('BLZUSDT', "1d", 200, 1.02, 0.98)
coin28 = Macdema('KAVAUSDT', "1d", 15, 1.02, 0.98)
coin29 = Macdema('CHZUSDT', "1d", 250, 1.02, 0.98)

coin31 = Macdema('QTUMUSDT', "1d", 8, 1.02, 0.98)
coin32 = Macdema('CHRUSDT', "1d", 150, 1.02, 0.98)
coin33 = Macdema('OCEANUSDT', "1d", 100, 1.02, 0.98)
coin34 = Macdema('ALPHAUSDT', "1d", 150,1.02, 0.98)


while True:
    coin2.dfall('ETHUSDT', "1d")
    time.sleep(15)
    coin1.dfall('BTCUSDT', "1d")
    time.sleep(15)
    coin3.dfall('ATOMUSDT', "1d")
    time.sleep(15)
    coin4.dfall('EOSUSDT', "1d")
    time.sleep(15)
    coin5.dfall('LITUSDT', "1d")
    time.sleep(15)
    coin6.dfall('BNBUSDT', "1d")
    time.sleep(15)
    coin7.dfall('CRVUSDT', "1d")
    time.sleep(15)
    coin8.dfall('THETAUSDT', "1d")
    time.sleep(15)
    coin9.dfall('XRPUSDT', "1d")
    time.sleep(15)
    coin10.dfall('RUNEUSDT', "1d")
    time.sleep(15)
    coin11.dfall('ARUSDT', "1d")
    time.sleep(15)
    coin12.dfall('DOTUSDT', "1d")
    time.sleep(15)
    coin13.dfall('ETCUSDT', "1d")
    time.sleep(15)
    coin14.dfall('ALGOUSDT', "1d")
    time.sleep(15)
    coin15.dfall('TRXUSDT', "1d")
    time.sleep(15)
    coin16.dfall('LRCUSDT', "1d")
    time.sleep(15)
    coin17.dfall('SANDUSDT', "1d")
    time.sleep(15)
    coin18.dfall('AVAXUSDT', "1d")
    time.sleep(15)
    coin19.dfall('COTIUSDT', "1d")
    time.sleep(15)
    coin20.dfall('LINKUSDT', "1d")
    time.sleep(15)
    coin21.dfall('NEARUSDT', "1d")
    time.sleep(15)

    coin24.dfall('MATICUSDT', "1d")
    time.sleep(15)
    coin25.dfall('BELUSDT', "1d")
    time.sleep(15)
    coin26.dfall('KNCUSDT', "1d")
    time.sleep(15)
    coin27.dfall('BLZUSDT', "1d")
    time.sleep(15)
    coin28.dfall('KAVAUSDT', "1d")
    time.sleep(15)
    coin29.dfall('CHZUSDT', "1d")
    time.sleep(15)

    coin31.dfall('QTUMUSDT', "1d")
    time.sleep(15)
    coin32.dfall('CHRUSDT', "1d")
    time.sleep(15)
    coin33.dfall('OCEANUSDT', "1d")
    time.sleep(15)
    coin34.dfall('ALPHAUSDT', "1d")
    time.sleep(15)




    time.sleep(4800)

