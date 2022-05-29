import ccxt,config
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

kesisimmacdsayac =0
kesisimmovaverage =0
longgiris =0
shortgiris =0
sayici_giris_control = 0
sheetsymbolx =0
sheetssymboly =0
macdlast = 0



class Macdema():


    def __init__(self,symbol,timeframe,quantity,buyvalue,sellvalue):
        self.symbol=symbol
        self.kesisimmovaverage=kesisimmovaverage
        self.kesisimmacdsayac=kesisimmacdsayac
        self.longgiris=longgiris
        self.shortgiris=shortgiris
        self.timeframe=timeframe
        self.sayici_giris_control=sayici_giris_control
        self.macdlast=macdlast
        self.quantity=quantity
        self.buyvalue=buyvalue
        self.sellvalue=sellvalue


    """
    def addspread(self,sheetsymbolx,sheetsymboly,movkesx,movkesy,
                  macdkesx,macdkesy,shortgirisx,shortgirisy,longirisx,
                  longgirisy,sayicikontx,sayicikonty):
        gc = gspread.service_account(filename='credentials.json')

        sh = gc.open_by_key('1jRT7SlWoqaEscBFEz9835rsyrh9m1TNR_HfnGpItTHU')
        worksheet = sh.sheet1
        worksheet.update_cell(sheetsymbolx, sheetsymboly, self.symbol)
        worksheet.update_cell(movkesx,movkesy,self.kesisimmovaverage)
        worksheet.update_cell( macdkesx, macdkesy, self.kesisimmacdsayac)
        worksheet.update_cell(shortgirisx, shortgirisy, self.shortgiris)
        worksheet.update_cell(longirisx, longgirisy, self.longgiris)
        worksheet.update_cell(sayicikontx, sayicikonty, self.sayici_giris_control)

    """






    def dfall(self,symbol,timeframe):


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
            if self.shortgiris==1 or self.longgiris==1:
                self.sayici_giris_control += 1
                if self.sayici_giris_control ==200:
                    print(symbol,timeframe,self.sayici_giris_control)
                    self.longgiris=0
                    self.shortgiris=0


            else:
                bars = exchange.fetch_ohlcv(symbol, timeframe=timeframe, since=None, limit=100)
                df = pd.DataFrame(bars, columns=["timestamp", "open", "high", "low", "close", "volume"])


                macddf = df.ta.macd(close='close', fast=12, slow=26, signal=9, append=True)
                client = Client(api_key=key.Pkey, api_secret=key.Skey)
                result = client.futures_account_balance(asset='USDT')  # bir listeden asset cektik
                balance = float(result[6]['withdrawAvailable'])  # with drawal codu ile aldık
                print (balance)



                x = (macddf.iloc[:, 1])
                self.macdlast = (x.iloc[-1])
                print(symbol)
                print(self.macdlast)
                df["slow macd"] = macddf.iloc[:, 0]

                macd = MACD(df["close"])

                df["macd"] = macd.macd_signal()
                # LOAD SLOW EMA
                slowEma = EMAIndicator(df["close"], float(12))

                df["Slow Ema"] = slowEma.ema_indicator()

                # LOAD FAST EMA
                FastEma = EMAIndicator(df["close"], float(26))
                df["Fast Ema"] = FastEma.ema_indicator()
                print (symbol,self.shortgiris,self.timeframe)
                print (symbol,self.longgiris,self.timeframe)
                print (symbol,self.kesisimmovaverage,self.timeframe)
                print (symbol,self.kesisimmacdsayac,self.timeframe)

                if self.shortgiris!=1 and self.longgiris!=1:
                    if self.kesisimmacdsayac == 0:
                        if (df["macd"][len(df.index) - 3] < df["slow macd"][len(df.index) - 3] and df["macd"][
                            len(df.index) - 2] > df["slow macd"][len(df.index) - 2]) or (
                                df["macd"][len(df.index) - 3] > df["slow macd"][len(df.index) - 3] and df["macd"][
                            len(df.index) - 2] < df["slow macd"][len(df.index) - 2]):
                            self.kesisimmacdsayac += 1
                            tele.telegram_bot("macdkesisim")
                            print(df["macd"])
                            print(df["slow macd"])
                            print(symbol, "macdkesisim",self.kesisimmacdsayac)
                if self.shortgiris != 1 and self.longgiris != 1:

                    if self.kesisimmovaverage == 0:

                        if (df["Fast Ema"][len(df.index) - 3] < df["Slow Ema"][len(df.index) - 3] and df["Fast Ema"][
                            len(df.index) - 2] > df["Slow Ema"][len(df.index) - 2]) or (
                                df["Fast Ema"][len(df.index) - 3] > df["Slow Ema"][len(df.index) - 3] and df["Fast Ema"][
                            len(df.index) - 2] < df["Slow Ema"][len(df.index) - 2]):
                            self.kesisimmovaverage += 1
                            tele.telegram_bot("movkesisim")
                            print(df["Slow Ema"])
                            print(df["Fast Ema"])
                            print(symbol,"movkesisim",self.kesisimmovaverage)
                    try:
                        price = client.futures_symbol_ticker(symbol=self.symbol, recvWindow=25000)

                        tp_price = func.price_sell_buy(price,self.buyvalue,self.sellvalue)
                        price_sell_new = tp_price[0]
                        price_buy_new = tp_price[1]
                        print(price_buy_new)
                        print(price_sell_new)
                        order_approve = func.open_order_number(self.symbol)
                        print("order approve", order_approve)
                        print("quantity",self.quantity)

                        if balance > 200:
                            if self.kesisimmovaverage == 1 and self.kesisimmacdsayac == 1:
                                if order_approve == 1:
                                    if self.macdlast > 0:
                                        print('long gir')
                                        tele.telegram_bot('long gir-macdmov_strategy')
                                        tele.telegram_bot(symbol)
                                        func.long_position(self.symbol, self.quantity,
                                                           price_sell_new)  # alıs olusturma fonk
                                        self.kesisimmovaverage = 0
                                        self.kesisimmacdsayac = 0
                                        self.longgiris += 1
                                        print(symbol, longgiris, "alis_sonrasi")
                                        time.sleep(10)
                                    else:
                                        print("short_gir")

                                        tele.telegram_bot("short_gir-macdmov_strategy")
                                        tele.telegram_bot(symbol)
                                        func.short_position(self.symbol, self.quantity,
                                                            price_buy_new)  # satıs olusturma fonk
                                        self.kesisimmovaverage = 0
                                        self.kesisimmacdsayac = 0
                                        self.shortgiris += 1
                                        print(symbol, shortgiris, "alis_sonrasi")

                            else:
                                tele.telegram_bot("islem sayisi 5 den fazlastrtegy2")
                        else:
                            print("balance 200 altında")

                    except:
                          tele.telegram_bot('fiyat alamadı')
        except ccxt.BaseError as Error:
            print("[ERROR] ", Error)



coin2=Macdema('ETHUSDT',"1h",0.015,1.01,0.991)
coin1=Macdema('BTCUSDT',"1h",0.001,1.01,0.991)
coin3=Macdema('ATOMUSDT',"1h",2,1.01,0.991)
coin4=Macdema('EOSUSDT',"1h",20,1.01,0.991)
coin5=Macdema('LITUSDT',"1h",40,1.01,0.991)
coin6=Macdema('ICPUSDT',"1h",4,1.01,0.991)
coin7=Macdema('CRVUSDT',"1h",22,1.01,0.991)
coin8=Macdema('THETAUSDT',"1h",20,1.01,0.991)
coin9=Macdema('XRPUSDT',"1h",60,1.01,0.991)
coin10=Macdema('RUNEUSDT',"1h",10,1.01,0.991)
coin11=Macdema('ARUSDT',"1h",2,1.01,0.991)
coin12=Macdema('DOTUSDT',"1h",3,1.01,0.991)
coin13=Macdema('ETCUSDT',"1h",1.5,1.01,0.991)
coin14=Macdema('ALGOUSDT',"1h",80,1.01,0.991)
coin15=Macdema('TRXUSDT',"1h",200,1.01,0.991)
coin16=Macdema('LRCUSDT',"1h",50,1.01,0.991)
coin17=Macdema('SANDUSDT',"1h",25,1.01,0.991)

coin2a=Macdema('ETHUSDT',"15m",0.015,1.007,0.993)
coin1a=Macdema('BTCUSDT',"15m",0.001,1.007,0.993)
coin3a=Macdema('ATOMUSDT',"15m",2,1.007,0.993)
coin4a=Macdema('EOSUSDT',"15m",20,1.007,0.993)
coin5a=Macdema('LITUSDT',"15m",40,1.007,0.993)
coin6a=Macdema('ICPUSDT',"15m",4,1.007,0.993)
coin7a=Macdema('CRVUSDT',"15m",22,1.007,0.993)
coin8a=Macdema('THETAUSDT',"15m",20,1.007,0.993)
coin9a=Macdema('XRPUSDT',"15m",60,1.007,0.993)
coin10a=Macdema('RUNEUSDT',"15m",10,1.007,0.993)
coin11a=Macdema('ARUSDT',"15m",2,1.007,0.993)
coin12a=Macdema('DOTUSDT',"15m",3,1.007,0.993)
coin13a=Macdema('ETCUSDT',"15m",1.5,1.007,0.993)
coin14a=Macdema('ALGOUSDT',"15m",80,1.007,0.993)
coin15a=Macdema('TRXUSDT',"15m",200,1.007,0.993)
coin16a=Macdema('LRCUSDT',"15m",50,1.007,0.993)
coin17a=Macdema('SANDUSDT',"15m",25,1.007,0.993)

coin2b=Macdema('ETHUSDT',"4h",0.015,1.015,0.985)
coin1b=Macdema('BTCUSDT',"4h",0.001,1.015,0.985)
coin3b=Macdema('ATOMUSDT',"4h",2,1.015,0.985)
coin4b=Macdema('EOSUSDT',"4h",20,1.015,0.985)
coin5b=Macdema('LITUSDT',"4h",40,1.015,0.985)
coin6b=Macdema('ICPUSDT',"4h",4,1.015,0.985)
coin7b=Macdema('CRVUSDT',"4h",22,1.015,0.985)
coin8b=Macdema('THETAUSDT',"4h",20,1.015,0.985)
coin9b=Macdema('XRPUSDT',"4h",60,1.015,0.985)
coin10b=Macdema('RUNEUSDT',"4h",10,1.015,0.985)
coin11b=Macdema('ARUSDT',"4h",2,1.015,0.985)
coin12b=Macdema('DOTUSDT',"4h",3,1.015,0.985)
coin13b=Macdema('ETCUSDT',"4h",1.5,1.015,0.985)
coin14b=Macdema('ALGOUSDT',"4h",80,1.015,0.985)
coin15b=Macdema('TRXUSDT',"4h",200,1.015,0.985)
coin16b=Macdema('LRCUSDT',"4h",50,1.015,0.985)
coin17b=Macdema('SANDUSDT',"4h",25,1.015,0.985)

while True:

    coin2.dfall('ETHUSDT',"1h")
    time.sleep(10)
    coin1.dfall('BTCUSDT',"1h")
    time.sleep(10)
    coin3.dfall('ATOMUSDT',"1h")
    time.sleep(10)
    coin4.dfall('EOSUSDT',"1h")
    time.sleep(10)
    coin5.dfall('LITUSDT',"1h")
    time.sleep(10)
    coin6.dfall('ICPUSDT',"1h")
    time.sleep(10)
    coin7.dfall('CRVUSDT',"1h")
    time.sleep(10)
    coin8.dfall('THETAUSDT',"1h")
    time.sleep(10)
    coin9.dfall('XRPUSDT',"1h")
    time.sleep(10)
    coin10.dfall('RUNEUSDT',"1h")
    time.sleep(10)
    coin11.dfall('ARUSDT',"1h")
    time.sleep(10)
    coin12.dfall('DOTUSDT',"1h")
    time.sleep(10)
    coin13.dfall('ETCUSDT',"1h")
    time.sleep(10)
    coin14.dfall('ALGOUSDT',"1h")
    time.sleep(10)
    coin15.dfall('TRXUSDT',"1h")
    time.sleep(10)
    coin16.dfall('LRCUSDT',"1h")
    time.sleep(10)
    coin17.dfall('SANDUSDT',"1h")

    coin2a.dfall('ETHUSDT', "15m")
    time.sleep(10)
    coin1a.dfall('BTCUSDT', "15m")
    time.sleep(10)
    coin3a.dfall('ATOMUSDT', "15m")
    time.sleep(10)
    coin4a.dfall('EOSUSDT', "15m")
    time.sleep(10)
    coin5a.dfall('LITUSDT', "15m")
    time.sleep(10)
    coin6a.dfall('ICPUSDT', "15m")
    time.sleep(10)
    coin7a.dfall('CRVUSDT', "15m")
    time.sleep(10)
    coin8a.dfall('THETAUSDT', "15m")
    time.sleep(10)
    coin9a.dfall('XRPUSDT', "15m")
    time.sleep(10)
    coin10a.dfall('RUNEUSDT', "15m")
    time.sleep(10)
    coin11a.dfall('ARUSDT', "15m")
    time.sleep(10)
    coin12a.dfall('DOTUSDT', "15m")
    time.sleep(10)
    coin13a.dfall('ETCUSDT', "15m")
    time.sleep(10)
    coin14a.dfall('ALGOUSDT', "15m")
    time.sleep(10)
    coin15a.dfall('TRXUSDT',"15m")
    time.sleep(10)
    coin16a.dfall('LRCUSDT', "15m")
    time.sleep(10)
    coin17a.dfall('SANDUSDT', "15m")

    coin2b.dfall('ETHUSDT', "4h")
    time.sleep(10)
    coin1b.dfall('BTCUSDT', "4h")
    time.sleep(10)
    coin3b.dfall('ATOMUSDT', "4h")
    time.sleep(10)
    coin4b.dfall('EOSUSDT', "4h")
    time.sleep(10)
    coin5b.dfall('LITUSDT', "4h")
    time.sleep(10)
    coin6b.dfall('ICPUSDT', "4h")
    time.sleep(10)
    coin7b.dfall('CRVUSDT', "4h")
    time.sleep(10)
    coin8b.dfall('THETAUSDT', "4h")
    time.sleep(10)
    coin9b.dfall('XRPUSDT', "4h")
    time.sleep(10)
    coin10b.dfall('RUNEUSDT', "4h")
    time.sleep(10)
    coin11b.dfall('ARUSDT', "4h")
    time.sleep(10)
    coin12b.dfall('DOTUSDT', "4h")
    time.sleep(10)
    coin13b.dfall('ETCUSDT', "4h")
    time.sleep(10)
    coin14b.dfall('ALGOUSDT', "4h")
    time.sleep(10)
    coin15b.dfall('TRXUSDT', "4h")
    time.sleep(10)
    coin16b.dfall('LRCUSDT', "4h")
    time.sleep(10)
    coin17b.dfall('SANDUSDT', "4h")




    time.sleep(25)




