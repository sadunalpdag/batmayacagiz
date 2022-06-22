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

sellsignal = 0
buysignal = 0
selltotalsignal = 0
buytotalsignal = 0
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
        self.sellsignal = sellsignal
        self.buysignal = buysignal
        self.selltotalsignal = selltotalsignal
        self.buytotalsignal = buytotalsignal



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
                                            limit=100)  # son 40 price cek pd yap


                df = pd.DataFrame(bars, columns=["timestamp", "open", "high", "low", "close", "volume"])


                df['stochrsi_k'] =ta.momentum.stochrsi_k(df.close)
                df['stochrsi_d'] = ta.momentum.stochrsi_d(df.close)


                for i in (8,26,50):
                    df['EMA_'+str(i)] = ta.trend.ema_indicator(df.close, window=i)
                df['atr'] = ta.volatility.average_true_range(df.high,df.low,df.close)
                macd = MACD(df["close"])
                df["macd"] = macd.macd_signal()

                df.dropna(inplace=True)
                def checkcrosssell(df):
                    seriessell =df['stochrsi_k'] < df['stochrsi_d']
                    return seriessell.diff()
                df['crosssell'] =checkcrosssell(df)
                #pd.options.display.max_columns = None
                #pd.options.display.max_rows = None

                def checkcrossbuy(df):
                    seriesbuy =df['stochrsi_k'] > df['stochrsi_d']
                    return seriesbuy.diff()
                df['crossbuy'] =checkcrossbuy(df)




                df['sellsignal'] = np.where((df.crosssell) & (df.close < df.EMA_8)  ,1,0)
                df['buysignal'] = np.where((df.crossbuy) & (df.close > df.EMA_8) , 1, 0)

                x = (df.iloc[:, 15])  # pd 1. colonu al
                self.sellsignal = (x.iloc[-1])  # pd 16. kolon son item

                y = (df.iloc[:, 16])  # pd 1. colonu al
                self.buysignal = (y.iloc[-1])  # pd 17. kolon son item

                w = (df.iloc[:, 7])  # pd 1. colonu al
                self.lastkvalue = (w.iloc[-1])  # pd 16. kolon son item

                if   self.sellsignal == 1  and self.lastkvalue > 0.6:
                      self.selltotalsignal =1
                elif self.buysignal == 1  and self.lastkvalue < 0.4:
                      self.buytotalsignal = 1
                #print ( self.lastkvalue)
                #print(df)

                if self.shortgiris != 1 and self.longgiris != 1 and self.buytotalsignal == 1 or self.selltotalsignal == 1:

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

                        if order_approve == 1 and self.buytotalsignal == 1 or self.selltotalsignal == 1 :

                            result = client.futures_account_balance(asset='USDT',
                                                                    recvWindow=49000)  # bir listeden asset cektik
                            balance = float(result[6]['withdrawAvailable'])  # with drawal codu ile aldık
                            if balance > 200:
                                try:
                                    if self.buytotalsignal == 1:
                                        print('long gir')
                                        buysignaltele = "buysignalstoch" + " " + self.symbol + " " + self.timeframe
                                        tele.telegram_bot(buysignaltele)

                                        self.buytotalsignal =0
                                        self.longgiris += 1
                                        func.long_position(self.symbol, self.quantity,
                                                           price_sell_new)  # alıs olusturma fonk

                                        time.sleep(10)
                                    elif self.selltotalsignal == 1:
                                         print("short_gir")

                                         sellsignaltele = "sellsignalstoch" + " " + self.symbol + " " + self.timeframe
                                         tele.telegram_bot(sellsignaltele)
                                         self.selftotalsignal = 0



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


coin2 = rsi_atr_ema('ETHUSDT', "2h", 0.015, 1.02, 0.98)
coin1 = rsi_atr_ema('BTCUSDT', "2h", 0.001, 1.02, 0.98)
coin3 = rsi_atr_ema('ATOMUSDT', "2h", 2, 1.02, 0.98)
coin4 = rsi_atr_ema('EOSUSDT', "2h", 20, 1.02, 0.98)
coin5 = rsi_atr_ema('LITUSDT', "2h", 40, 1.02, 0.98)
coin6 = rsi_atr_ema('BNBUSDT', "2h", 0.1, 1.02, 0.98)

coin7 = rsi_atr_ema('CRVUSDT', "2h", 22, 1.02, 0.98)
coin8 = rsi_atr_ema('THETAUSDT', "2h", 20, 1.02, 0.98)
coin9 = rsi_atr_ema('XRPUSDT', "2h", 10, 1.02, 0.98)
coin10 = rsi_atr_ema('RUNEUSDT', "2h", 10, 1.02, 0.98)
coin11 = rsi_atr_ema('ARUSDT', "2h", 2, 1.02, 0.98)
coin12 = rsi_atr_ema('DOTUSDT', "2h", 3, 1.02, 0.98)
coin13 = rsi_atr_ema('ETCUSDT', "2h", 1.5, 1.02, 0.98)
coin14 = rsi_atr_ema('ALGOUSDT', "2h", 80, 1.02, 0.98)
coin15 = rsi_atr_ema('TRXUSDT', "2h", 200, 1.02, 0.98)
coin16 = rsi_atr_ema('LRCUSDT', "2h", 50, 1.02, 0.98)
coin17 = rsi_atr_ema('SANDUSDT', "2h", 25, 1.02, 0.98)
coin18 = rsi_atr_ema('AVAXUSDT', "2h", 1, 1.02, 0.98)
coin19 = rsi_atr_ema('COTIUSDT', "2h", 220, 1.02, 0.98)
coin20 = rsi_atr_ema('LINKUSDT', "2h", 4, 1.02, 0.98)
coin21 = rsi_atr_ema('NEARUSDT', "2h", 9, 1.02, 0.98)

coin24 = rsi_atr_ema('MATICUSDT', "2h", 40, 1.02, 0.98)
coin25 = rsi_atr_ema('BELUSDT', "2h", 30, 1.02, 0.98)
coin26 = rsi_atr_ema('KNCUSDT', "2h", 20, 1.02, 0.98)
coin27 = rsi_atr_ema('BLZUSDT', "2h", 200, 1.02, 0.98)
coin28 = rsi_atr_ema('KAVAUSDT', "2h", 15, 1.02, 0.98)
coin29 = rsi_atr_ema('CHZUSDT', "2h", 250, 1.02, 0.98)

coin31 = rsi_atr_ema('QTUMUSDT', "2h", 8, 1.02, 0.98)
coin32 = rsi_atr_ema('CHRUSDT', "2h", 150, 1.02, 0.98)
coin33 = rsi_atr_ema('OCEANUSDT', "2h", 100, 1.02, 0.98)
coin34 = rsi_atr_ema('ALPHAUSDT', "2h", 150,1.02, 0.98)


while True:
    coin2.dfall('ETHUSDT', "2h")
    time.sleep(10)
    coin1.dfall('BTCUSDT', "2h")
    time.sleep(10)
    coin3.dfall('ATOMUSDT', "2h")
    time.sleep(10)
    coin4.dfall('EOSUSDT', "2h")
    time.sleep(10)
    coin5.dfall('LITUSDT', "2h")
    time.sleep(10)
    coin6.dfall('BNBUSDT', "2h")
    time.sleep(10)
    coin7.dfall('CRVUSDT', "2h")
    time.sleep(10)
    coin8.dfall('THETAUSDT', "2h")
    time.sleep(10)
    coin9.dfall('XRPUSDT', "2h")
    time.sleep(10)
    coin10.dfall('RUNEUSDT', "2h")
    time.sleep(10)
    coin11.dfall('ARUSDT', "2h")
    time.sleep(10)
    coin12.dfall('DOTUSDT', "2h")
    time.sleep(10)
    coin13.dfall('ETCUSDT', "2h")
    time.sleep(10)
    coin14.dfall('ALGOUSDT', "2h")
    time.sleep(10)
    coin15.dfall('TRXUSDT', "2h")
    time.sleep(10)
    coin16.dfall('LRCUSDT', "2h")
    time.sleep(10)
    coin17.dfall('SANDUSDT', "2h")
    time.sleep(10)
    coin18.dfall('AVAXUSDT', "2h")
    time.sleep(10)
    coin19.dfall('COTIUSDT', "2h")
    time.sleep(10)
    coin20.dfall('LINKUSDT', "2h")
    time.sleep(10)
    coin21.dfall('NEARUSDT', "2h")
    time.sleep(10)

    coin24.dfall('MATICUSDT', "2h")
    time.sleep(10)
    coin25.dfall('BELUSDT', "2h")
    time.sleep(10)
    coin26.dfall('KNCUSDT', "2h")
    time.sleep(10)
    coin27.dfall('BLZUSDT', "2h")
    time.sleep(10)
    coin28.dfall('KAVAUSDT', "2h")
    time.sleep(10)
    coin29.dfall('CHZUSDT', "2h")
    time.sleep(10)

    coin31.dfall('QTUMUSDT', "2h")
    time.sleep(10)
    coin32.dfall('CHRUSDT', "2h")
    time.sleep(10)
    coin33.dfall('OCEANUSDT', "2h")
    time.sleep(10)
    coin34.dfall('ALPHAUSDT', "2h")
    time.sleep(10)

    tele.telegram_bot('server online4')
    time.sleep(4800)