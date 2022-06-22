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
import ta
import numpy as np
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

class rsi_atr_ema():

    def __init__(self, symbol, timeframe, quantity, buyvalue, sellvalue):
        self.symbol = symbol
        self.longgiris = longgiris
        self.shortgiris = shortgiris
        self.timeframe = timeframe
        self.sayici_giris_control = sayici_giris_control
        self.quantity = quantity
        self.buyvalue = buyvalue
        self.sellvalue = sellvalue
        self.kesisimmacdsayac = kesisimmacdsayac



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
                                            limit=200)  # son 40 price cek pd yap
                df = pd.DataFrame(bars, columns=["timestamp", "open", "high", "low", "close", "volume"])

                df['stochrsi_k'] =ta.momentum.stochrsi_k(df.close)
                df['stochrsi_d'] = ta.momentum.stochrsi_d(df.close)

                for i in (8,14,50):
                    df['EMA_'+str(i)] = ta.trend.ema_indicator(df.close, window=i)
                df['atr'] = ta.volatility.average_true_range(df.high,df.low,df.close)
                macd = MACD(df["close"])
                df["macd"] = macd.macd_signal()

                df.dropna(inplace=True)
                def checkcross(df):
                    series =df['stochrsi_k'] > df['stochrsi_d']
                    return series.diff()
                df['cross'] =checkcross(df)
                df['TP'] = df.close + (df.atr)


                df['Buysignal'] = np.where((df.macd>0) & (df.cross) & (df.close > df.EMA_8) & (df.EMA_14 < df.EMA_8) & (df.EMA_50 < df.EMA_14),1,0)
                x= df.loc[df['Buysignal'] == 1]
                print (x)







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


coin2 = rsi_atr_ema('TRXUSDT', "4h", 0.015, 1.02, 0.98)


while True:
    coin2.dfall('TRXUSDT', "4h")

    tele.telegram_bot('server online4')
    time.sleep(4800)