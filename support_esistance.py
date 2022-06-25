import ccxt, config
import pandas as pd
from candlestick import candlestick
import requests

import time
import send_msg as tele
import pandas_ta as ta
import functions as func
import key
from binance.client import Client
import firebase_admin
from firebase_admin import credentials, firestore


longgiris = 0
shortgiris = 0
sayici_giris_control = 0
sheetsymbolx = 0
sheetssymboly = 0
macdlast = 0
engulfing = 0
last_elementbullish =False
last_elementbearish =False
kimlik = credentials.Certificate("firebase/emaclass-firebase-adminsdk-zivwq-88b53bed66.json")

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
        self.last_elementbullish=last_elementbullish
        self.last_elementbearish=last_elementbearish



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
                if self.sayici_giris_control == 3:
                    print(symbol, timeframe, self.sayici_giris_control)
                    self.longgiris = 0
                    self.shortgiris = 0
                    self.sayici_giris_control = 0


            else:

                candles = requests.get('https://api.binance.com/api/v1/klines?symbol='+self.symbol+'&interval='+self.timeframe)
                candles_dict = candles.json()

                candles_df = pd.DataFrame(candles_dict,
                                          columns=['T', 'open', 'high', 'low', 'close', 'V', 'CT', 'QV', 'N', 'TB',
                                                   'TQ', 'I'])

                candles_df['T'] = pd.to_datetime(candles_df['T'], unit='ms')

                target = 'bearish_engulfing'
                candles_df = candlestick.bearish_engulfing(candles_df, target=target)
                target1 = 'bullish_engulfing'
                candles_df = candlestick.bullish_engulfing(candles_df, target=target1)
                self.last_elementbullish = candles_df["bullish_engulfing"].iloc[-1]
                self.last_elementbearish = candles_df["bearish_engulfing"].iloc[-1]



                if self.last_elementbullish == True:
                    last_elementbearish_fire="Bullish"
                else:
                    last_elementbearish_fire="nothing"
                if self.last_elementbearish == True:
                    last_elementbullish_fire="Bearish"
                else:
                    last_elementbullish_fire="nothing"


                print (self.last_elementbearish)
                print (self.last_elementbullish)


                if self.shortgiris != 1 and self.longgiris != 1:

                    db = firestore.client()  # db e baglantı

                    document = db.collection("engulfing").document(self.symbol)
                    

                    document2 = db.collection("data2").document("balance")

                    engulfing = document.get().to_dict()

                    data2 = document2.get().to_dict()

                    document.set({
                        "symbol": self.symbol,
                        "engulfing_bullish": last_elementbullish_fire,
                        "engulfing_bearish" : last_elementbearish_fire,
                        "timeframe": self.timeframe

                    })

                    try:
                        client = Client(api_key=key.Pkey, api_secret=key.Skey)
                        result = client.futures_account_balance(asset='USDT',
                                                                recvWindow=49000)  # bir listeden asset cektik
                        balance = float(result[6]['withdrawAvailable'])
                        document2.set({
                            "balance": balance,
                        })
                        price = client.futures_symbol_ticker(symbol=self.symbol, recvWindow=45000)

                        tp_price = func.price_sell_buy(price, self.buyvalue, self.sellvalue)
                        price_sell_new = tp_price[0]
                        price_buy_new = tp_price[1]
                        print(price_buy_new)
                        print(price_sell_new)
                        order_approve = func.open_order_number(self.symbol)
                        print("order approve", order_approve)
                        print("quantity", self.quantity)
                        if self.last_elementbullish =="Bullish" or self.last_elementbearish=="Bearish" :
                            if order_approve == 1:
    
                                if balance > 200:
                                    try:
                                        if self.last_elementbullish =="Bullish":
                                            print('long gir')
                                            tele.telegram_bot('long gir-enfulging_strategy')
                                            tele.telegram_bot(symbol)
                                            self.longgiris += 1
                                            func.long_position(self.symbol, self.quantity,
                                                               price_sell_new)  # alıs olusturma fonk

                                            time.sleep(30)
                                        elif self.last_elementbearish=="Bearish":
                                            print("short_gir")

                                            tele.telegram_bot("short_gir-enfulging_strategy")
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
                            print("setup olusmadı")

                    except:
                        tele.telegram_bot('fiyat alamadı2')
        except ccxt.BaseError as Error:
            print("[ERROR] ", Error)

coin2 = Macdema('YFIUSDT', "2h", 0.005, 1.01, 0.991)
coin1 = Macdema('HNTUSDT', "2h", 3, 1.01, 0.991)
coin3 = Macdema('SUSHIUSDT', "2h", 30, 1.01, 0.991)
coin4 = Macdema('EOSUSDT', "2h", 20, 1.01, 0.991)
coin5 = Macdema('LITUSDT', "2h", 40, 1.01, 0.991)
coin6 = Macdema('BNBUSDT', "2h", 0.1, 1.01, 0.991)

coin7 = Macdema('1INCHUSDT', "2h", 45, 1.01, 0.991)
coin8 = Macdema('THETAUSDT', "2h", 20, 1.01, 0.991)
coin9 = Macdema('XRPUSDT', "2h", 60, 1.01, 0.991)
coin10 = Macdema('DYDXUSDT', "2h", 22, 1.01, 0.991)
coin11 = Macdema('ARUSDT', "2h", 2, 1.01, 0.991)
coin12 = Macdema('DOTUSDT', "2h", 3, 1.01, 0.991)
coin13 = Macdema('ETCUSDT', "2h", 1.5, 1.01, 0.991)
coin14 = Macdema('ALGOUSDT', "2h", 80, 1.01, 0.991)
coin15 = Macdema('TRXUSDT', "2h", 200, 1.01, 0.991)
coin16 = Macdema('LRCUSDT', "2h", 50, 1.01, 0.991)
coin17 = Macdema('SANDUSDT', "2h", 25, 1.01, 0.991)
coin18 = Macdema('AVAXUSDT', "2h", 1, 1.01, 0.991)
coin19 = Macdema('COTIUSDT', "2h", 220, 1.01, 0.991)
coin20 = Macdema('LINKUSDT', "2h", 4, 1.01, 0.991)
coin21 = Macdema('NEARUSDT', "2h", 9, 1.01, 0.991)

coin24 = Macdema('MATICUSDT', "2h", 40, 1.01, 0.991)
coin25 = Macdema('BELUSDT', "2h", 30, 1.01, 0.991)
coin26 = Macdema('KNCUSDT', "2h", 20, 1.01, 0.991)
coin27 = Macdema('BLZUSDT', "2h", 200, 1.01, 0.991)
coin28 = Macdema('KAVAUSDT', "2h", 15, 1.01, 0.991)
coin29 = Macdema('CHZUSDT', "2h", 250, 1.01, 0.991)

coin31 = Macdema('QTUMUSDT', "2h", 8, 1.01, 0.991)
coin32 = Macdema('CHRUSDT', "2h", 150, 1.01, 0.991)
coin33 = Macdema('OCEANUSDT', "2h", 100, 1.01, 0.991)
coin34 = Macdema('ALPHAUSDT', "2h", 150, 1.01, 0.991)

coin2a = Macdema('YFIUSDT', "4h", 0.005, 1.02, 0.98)
coin1a = Macdema('HNTUSDT', "4h", 3, 1.02, 0.98)
coin3a = Macdema('SUSHIUSDT', "4h", 30, 1.02, 0.98)
coin4a = Macdema('EOSUSDT', "4h", 20, 1.02, 0.98)
coin5a = Macdema('LITUSDT', "4h", 40, 1.02, 0.98)
coin6a = Macdema('BNBUSDT', "4h", 0.1, 1.007, 0.9993)

coin7a = Macdema('1INCHUSDT', "4h", 45, 1.02, 0.98)
coin8a = Macdema('THETAUSDT', "4h", 20, 1.02, 0.98)
coin9a = Macdema('XRPUSDT', "4h", 60, 1.02, 0.98)
coin10a = Macdema('DYDXUSDT', "4h", 22, 1.02, 0.98)
coin11a = Macdema('ARUSDT', "4h", 2, 1.02, 0.98)
coin12a = Macdema('DOTUSDT', "4h", 3, 1.02, 0.98)
coin13a = Macdema('ETCUSDT', "4h", 1.5, 1.02, 0.98)
coin14a = Macdema('ALGOUSDT', "4h", 80, 1.02, 0.98)
coin15a = Macdema('TRXUSDT', "4h", 200, 1.02, 0.98)
coin16a = Macdema('LRCUSDT', "4h", 50, 1.02, 0.98)
coin17a = Macdema('SANDUSDT', "4h", 25, 1.02, 0.98)
coin18a = Macdema('AVAXUSDT', "4h", 1, 1.02, 0.98)

coin19a = Macdema('COTIUSDT', "4h", 220, 1.02, 0.98)
coin20a = Macdema('LINKUSDT', "4h", 4, 1.02, 0.98)
coin21a = Macdema('NEARUSDT', "4h", 9, 1.02, 0.98)

coin24a = Macdema('MATICUSDT', "4h", 40, 1.02, 0.98)
coin25a = Macdema('BELUSDT', "4h", 30, 1.02, 0.98)
coin26a = Macdema('KNCUSDT', "4h", 20, 1.02, 0.98)
coin27a = Macdema('BLZUSDT', "4h", 200, 1.02, 0.98)
coin28a = Macdema('KAVAUSDT', "4h", 15, 1.02, 0.98)
coin29a = Macdema('CHZUSDT', "4h", 250, 1.02, 0.98)

coin31a = Macdema('QTUMUSDT', "4h", 8, 1.02, 0.98)
coin32a = Macdema('CHRUSDT', "4h", 150, 1.02, 0.98)
coin33a = Macdema('OCEANUSDT', "4h", 100, 1.02, 0.98)
coin34a = Macdema('ALPHAUSDT', "4h", 150, 1.02, 0.98)

while True:
    coin2.dfall('YFIUSDT', "2h")
    time.sleep(30)
    coin1.dfall('HNTUSDT', "2h")
    time.sleep(30)
    coin3.dfall('SUSHIUSDT', "2h")
    time.sleep(30)
    coin4.dfall('EOSUSDT', "2h")
    time.sleep(30)
    coin5.dfall('LITUSDT', "2h")
    time.sleep(30)
    coin6.dfall('BNBUSDT', "2h")
    time.sleep(30)
    coin7.dfall('1INCHUSDT', "2h")
    time.sleep(30)
    coin8.dfall('THETAUSDT', "2h")
    time.sleep(30)
    coin9.dfall('XRPUSDT', "2h")
    time.sleep(30)
    coin10.dfall('DYDXUSDT', "2h")
    time.sleep(30)
    coin11.dfall('ARUSDT', "2h")
    time.sleep(30)
    coin12.dfall('DOTUSDT', "2h")
    time.sleep(30)
    coin13.dfall('ETCUSDT', "2h")
    time.sleep(30)
    coin14.dfall('ALGOUSDT', "2h")
    time.sleep(30)
    coin15.dfall('TRXUSDT', "2h")
    time.sleep(30)
    coin16.dfall('LRCUSDT', "2h")
    time.sleep(30)
    coin17.dfall('SANDUSDT', "2h")
    time.sleep(30)
    coin18.dfall('AVAXUSDT', "2h")
    time.sleep(30)
    coin19.dfall('COTIUSDT', "2h")
    time.sleep(30)
    coin20.dfall('LINKUSDT', "2h")
    time.sleep(30)
    coin21.dfall('NEARUSDT', "2h")
    time.sleep(30)

    coin24.dfall('MATICUSDT', "2h")
    time.sleep(30)
    coin25.dfall('BELUSDT', "2h")
    time.sleep(30)
    coin26.dfall('KNCUSDT', "2h")
    time.sleep(30)
    coin27.dfall('BLZUSDT', "2h")
    time.sleep(30)
    coin28.dfall('KAVAUSDT', "2h")
    time.sleep(30)
    coin29.dfall('CHZUSDT', "2h")
    time.sleep(30)

    coin31.dfall('QTUMUSDT', "2h")
    time.sleep(30)
    coin32.dfall('CHRUSDT', "2h")
    time.sleep(30)
    coin33.dfall('OCEANUSDT', "2h")
    time.sleep(30)
    coin34.dfall('ALPHAUSDT', "2h")
    time.sleep(30)

    coin2a.dfall('YFIUSDT', "4h")
    time.sleep(30)
    coin1a.dfall('HNTUSDT', "4h")
    time.sleep(30)
    coin3a.dfall('SUSHIUSDT', "4h")
    time.sleep(30)
    coin4a.dfall('EOSUSDT', "4h")
    time.sleep(30)
    coin5a.dfall('LITUSDT', "4h")
    time.sleep(30)
    coin6a.dfall('BNBUSDT', "4h")
    time.sleep(30)
    coin7a.dfall('1INCHUSDT', "4h")
    time.sleep(30)
    coin8a.dfall('THETAUSDT', "4h")
    time.sleep(30)
    coin9a.dfall('XRPUSDT', "4h")
    time.sleep(30)
    coin10a.dfall('DYDXUSDT', "4h")
    time.sleep(30)
    coin11a.dfall('ARUSDT', "4h")
    time.sleep(30)
    coin12a.dfall('DOTUSDT', "4h")
    time.sleep(30)
    coin13a.dfall('ETCUSDT', "4h")
    time.sleep(30)
    coin14a.dfall('ALGOUSDT', "4h")
    time.sleep(30)
    coin15a.dfall('TRXUSDT', "4h")
    time.sleep(30)
    coin16a.dfall('LRCUSDT', "4h")
    time.sleep(30)
    coin17a.dfall('SANDUSDT', "4h")
    time.sleep(30)
    coin18a.dfall('AVAXUSDT', "4h")
    time.sleep(30)
    coin19a.dfall('COTIUSDT', "4h")
    time.sleep(30)
    coin20a.dfall('LINKUSDT', "4h")
    time.sleep(30)
    coin21a.dfall('NEARUSDT', "4h")
    time.sleep(30)

    coin24a.dfall('MATICUSDT', "4h")
    time.sleep(30)
    coin25a.dfall('BELUSDT', "4h")
    time.sleep(30)
    coin26a.dfall('KNCUSDT', "4h")
    time.sleep(30)
    coin27a.dfall('BLZUSDT', "4h")
    time.sleep(30)
    coin28a.dfall('KAVAUSDT', "4h")
    time.sleep(30)
    coin29a.dfall('CHZUSDT', "4h")
    time.sleep(30)

    coin31a.dfall('QTUMUSDT', "4h")
    time.sleep(30)
    coin32a.dfall('CHRUSDT', "4h")
    time.sleep(30)
    coin33a.dfall('OCEANUSDT', "4h")
    time.sleep(30)
    coin34a.dfall('ALPHAUSDT', "4h")
    time.sleep(30)

    tele.telegram_bot('server online5')
    time.sleep(4800)





















