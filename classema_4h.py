import ccxt, config
import pandas as pd
from ta.trend import EMAIndicator
from ta.trend import MACD
import time
import send_msg as tele
import pandas_ta as ta
import functions as func
import key
from binance.client import Client
import gspread

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

        exchange = ccxt.binance({
            "apiKey": config.apiKey,
            "secret": config.secretKey,

            'options': {
                'defaultType': 'future'
            },
            'enableRateLimit': True,
            'adjustForTimeDifference': True
        })



        try:

            order_approve = func.open_order_number(self.symbol)
            if self.shortgiris == 1 or self.longgiris == 1 or order_approve == 0:  # alıs satıstan sonra 100 cycledan sonra tekrar işleme açma
                self.sayici_giris_control += 1
                if self.sayici_giris_control == 15:
                    print(symbol, timeframe, self.sayici_giris_control)
                    self.longgiris = 0
                    self.shortgiris = 0
                    self.sayici_giris_control = 0


            else:
                bars = exchange.fetch_ohlcv(symbol, timeframe=timeframe, since=None,
                                            limit=40)  # son 40 price cek pd yap
                df = pd.DataFrame(bars, columns=["timestamp", "open", "high", "low", "close", "volume"])

                macddf = df.ta.macd(close='close', fast=12, slow=26, signal=9, append=True)
                print (macddf)
                x = (macddf.iloc[:, 1])  # pd 1. colonu al
                self.macdlast = (x.iloc[-1])  # pd 1. kolon son item



                y = macddf.iloc[:, 0]
                self.fastmacd = (y.iloc[-1])

                z = macddf.iloc[:, 2]
                self.slowmacd = (z.iloc[-1])



                macd = MACD(df["close"])

                df["macd"] = macd.macd_signal()
                df["slow macd"] = macddf.iloc[:, 0]






                if self.shortgiris != 1 and self.longgiris != 1:
                    if self.kesisimmacdsayac == 0:
                        if (df["macd"][len(df.index) - 2] < df["slow macd"][len(df.index) - 2] and df["macd"][
                            len(df.index) - 1] > df["slow macd"][len(df.index) - 1]) or (
                                df["macd"][len(df.index) - 2] > df["slow macd"][len(df.index) - 2] and df["macd"][
                            len(df.index) - 1] < df["slow macd"][len(df.index) - 1]):
                            self.kesisimmacdsayac += 1
                            macdkesisim = "macdkesisim"" " + self.symbol + " " + self.timeframe
                            tele.telegram_bot(macdkesisim)
                            print(df["macd"])
                            print(df["slow macd"])
                            print(symbol, "macdkesisim", self.kesisimmacdsayac)

                    try:
                        client = Client(api_key=key.Pkey, api_secret=key.Skey)
                        price = client.futures_symbol_ticker(symbol=self.symbol, recvWindow=45000)
                        tp_price = func.price_sell_buy(price, self.buyvalue, self.sellvalue)
                        price_sell_new = tp_price[0]
                        price_buy_new = tp_price[1]
                        print(price_buy_new)
                        print(price_sell_new)
                        order_approve = func.open_order_number(self.symbol)
                        print("order approve", order_approve)
                        print("quantity", self.quantity)
                        if  self.kesisimmacdsayac == 1:
                            if order_approve == 1:

                                result = client.futures_account_balance(asset='USDT',
                                                                        recvWindow=49000)  # bir listeden asset cektik
                                balance = float(result[6]['withdrawAvailable'])  # with drawal codu ile aldık
                                if balance > 200:
                                    try:
                                        if  self.macdlast > 0:
                                            print('long gir')
                                            tele.telegram_bot('long gir-macd2h_strategy')
                                            tele.telegram_bot(symbol)

                                            self.kesisimmacdsayac = 0
                                            self.longgiris += 1
                                            func.long_position(self.symbol, self.quantity,
                                                               price_sell_new)  # alıs olusturma fonk

                                            time.sleep(10)
                                        else:
                                            print("short_gir")

                                            tele.telegram_bot("'long gir-macd2h_strategy'")
                                            tele.telegram_bot(symbol)

                                            self.kesisimmacdsayac = 0
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
    time.sleep(60)
    coin1.dfall('BTCUSDT', "2h")
    time.sleep(60)
    coin3.dfall('ATOMUSDT', "2h")
    time.sleep(60)
    coin4.dfall('EOSUSDT', "2h")
    time.sleep(60)
    coin5.dfall('LITUSDT', "2h")
    time.sleep(60)
    coin6.dfall('BNBUSDT', "2h")
    time.sleep(60)
    coin7.dfall('CRVUSDT', "2h")
    time.sleep(60)
    coin8.dfall('THETAUSDT', "2h")
    time.sleep(60)
    coin9.dfall('XRPUSDT', "2h")
    time.sleep(60)
    coin10.dfall('RUNEUSDT', "2h")
    time.sleep(60)
    coin11.dfall('ARUSDT', "2h")
    time.sleep(60)
    coin12.dfall('DOTUSDT', "2h")
    time.sleep(60)
    coin13.dfall('ETCUSDT', "2h")
    time.sleep(60)
    coin14.dfall('ALGOUSDT', "2h")
    time.sleep(60)
    coin15.dfall('TRXUSDT', "2h")
    time.sleep(60)
    coin16.dfall('LRCUSDT', "2h")
    time.sleep(60)
    coin17.dfall('SANDUSDT', "2h")
    time.sleep(60)
    coin18.dfall('AVAXUSDT', "2h")
    time.sleep(60)
    coin19.dfall('COTIUSDT', "2h")
    time.sleep(60)
    coin20.dfall('LINKUSDT', "2h")
    time.sleep(60)
    coin21.dfall('NEARUSDT', "2h")
    time.sleep(60)

    coin24.dfall('MATICUSDT', "2h")
    time.sleep(60)
    coin25.dfall('BELUSDT', "2h")
    time.sleep(60)
    coin26.dfall('KNCUSDT', "2h")
    time.sleep(60)
    coin27.dfall('BLZUSDT', "2h")
    time.sleep(60)
    coin28.dfall('KAVAUSDT', "2h")
    time.sleep(60)
    coin29.dfall('CHZUSDT', "2h")
    time.sleep(60)

    coin31.dfall('QTUMUSDT', "2h")
    time.sleep(60)
    coin32.dfall('CHRUSDT', "2h")
    time.sleep(60)
    coin33.dfall('OCEANUSDT', "2h")
    time.sleep(60)
    coin34.dfall('ALPHAUSDT', "2h")
    time.sleep(60)



    tele.telegram_bot('server online3')
    time.sleep(4800)










