from tradingview_ta import TA_Handler, Interval, Exchange
import pandas as pd
import time
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

coin2 = Macdema('ETHUSDT', "2h", 0.015, 1.02, 0.98)
coin1 = Macdema('BTCUSDT', "2h", 0.001, 1.02, 0.98)
coin3 = Macdema('ATOMUSDT', "2h", 2, 1.02, 0.98)
coin4 = Macdema('EOSUSDT', "2h", 20, 1.02, 0.98)
coin5 = Macdema('LITUSDT', "2h", 40, 1.02, 0.98)
coin6 = Macdema('BNBUSDT', "2h", 0.1, 1.02, 0.98)

coin7 = Macdema('CRVUSDT', "2h", 22, 1.02, 0.98)
coin8 = Macdema('THETAUSDT', "2h", 20, 1.02, 0.98)
coin9 = Macdema('XRPUSDT', "2h", 60, 1.02, 0.98)
coin10 = Macdema('RUNEUSDT', "2h", 10, 1.02, 0.98)
coin11 = Macdema('ARUSDT', "2h", 2, 1.02, 0.98)
coin12 = Macdema('DOTUSDT', "2h", 3, 1.02, 0.98)
coin13 = Macdema('ETCUSDT', "2h", 1.5, 1.02, 0.98)
coin14 = Macdema('ALGOUSDT', "2h", 80, 1.02, 0.98)
coin15 = Macdema('TRXUSDT', "2h", 200, 1.02, 0.98)
coin16 = Macdema('LRCUSDT', "2h", 50, 1.02, 0.98)
coin17 = Macdema('SANDUSDT', "2h", 25, 1.02, 0.98)
coin18 = Macdema('AVAXUSDT', "2h", 1, 1.02, 0.98)
coin19 = Macdema('COTIUSDT', "2h", 220, 1.02, 0.98)
coin20 = Macdema('LINKUSDT', "2h", 4, 1.02, 0.98)
coin21 = Macdema('NEARUSDT', "2h", 9, 1.02, 0.98)

coin24 = Macdema('MATICUSDT', "2h", 40, 1.02, 0.98)
coin25 = Macdema('BELUSDT', "2h", 30, 1.02, 0.98)
coin26 = Macdema('KNCUSDT', "2h", 20, 1.02, 0.98)
coin27 = Macdema('BLZUSDT', "2h", 200, 1.02, 0.98)
coin28 = Macdema('KAVAUSDT', "2h", 15, 1.02, 0.98)
coin29 = Macdema('CHZUSDT', "2h", 250, 1.02, 0.98)

coin31 = Macdema('QTUMUSDT', "2h", 8, 1.02, 0.98)
coin32 = Macdema('CHRUSDT', "2h", 150, 1.02, 0.98)
coin33 = Macdema('OCEANUSDT', "2h", 100, 1.02, 0.98)
coin34 = Macdema('ALPHAUSDT', "2h", 150,1.02, 0.98)


while True:
    coin2.dfall('ETHUSDT', "2h")
    time.sleep(15)
    coin1.dfall('BTCUSDT', "2h")
    time.sleep(15)
    coin3.dfall('ATOMUSDT', "2h")
    time.sleep(15)
    coin4.dfall('EOSUSDT', "2h")
    time.sleep(15)
    coin5.dfall('LITUSDT', "2h")
    time.sleep(15)
    coin6.dfall('BNBUSDT', "2h")
    time.sleep(15)
    coin7.dfall('CRVUSDT', "2h")
    time.sleep(15)
    coin8.dfall('THETAUSDT', "2h")
    time.sleep(15)
    coin9.dfall('XRPUSDT', "2h")
    time.sleep(15)
    coin10.dfall('RUNEUSDT', "2h")
    time.sleep(15)
    coin11.dfall('ARUSDT', "2h")
    time.sleep(15)
    coin12.dfall('DOTUSDT', "2h")
    time.sleep(15)
    coin13.dfall('ETCUSDT', "2h")
    time.sleep(15)
    coin14.dfall('ALGOUSDT', "2h")
    time.sleep(15)
    coin15.dfall('TRXUSDT', "2h")
    time.sleep(15)
    coin16.dfall('LRCUSDT', "2h")
    time.sleep(15)
    coin17.dfall('SANDUSDT', "2h")
    time.sleep(15)
    coin18.dfall('AVAXUSDT', "2h")
    time.sleep(15)
    coin19.dfall('COTIUSDT', "2h")
    time.sleep(15)
    coin20.dfall('LINKUSDT', "2h")
    time.sleep(15)
    coin21.dfall('NEARUSDT', "2h")
    time.sleep(15)

    coin24.dfall('MATICUSDT', "2h")
    time.sleep(15)
    coin25.dfall('BELUSDT', "2h")
    time.sleep(15)
    coin26.dfall('KNCUSDT', "2h")
    time.sleep(15)
    coin27.dfall('BLZUSDT', "2h")
    time.sleep(15)
    coin28.dfall('KAVAUSDT', "2h")
    time.sleep(15)
    coin29.dfall('CHZUSDT', "2h")
    time.sleep(15)

    coin31.dfall('QTUMUSDT', "2h")
    time.sleep(15)
    coin32.dfall('CHRUSDT', "2h")
    time.sleep(15)
    coin33.dfall('OCEANUSDT', "2h")
    time.sleep(15)
    coin34.dfall('ALPHAUSDT', "2h")
    time.sleep(15)




    time.sleep(4800)

