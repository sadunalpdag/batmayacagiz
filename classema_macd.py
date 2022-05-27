import ccxt,config
import pandas as pd
from ta.trend import EMAIndicator
from ta.trend import MACD
import time
import send_msg as tele
import pandas_ta as ta


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


    def __init__(self,symbol,timeframe):
        self.symbol=symbol
        self.kesisimmovaverage=kesisimmovaverage
        self.kesisimmacdsayac=kesisimmacdsayac
        self.longgiris=longgiris
        self.shortgiris=shortgiris
        self.timeframe=timeframe
        self.sayici_giris_control=sayici_giris_control
        self.macdlast=macdlast



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








    def dfall(self,symbol,timeframe):


        exchange = ccxt.binance({
            "apiKey": config.apiKey,
            "secret": config.secretKey,

            'options': {
                'defaultType': 'future'
            },
            'enableRateLimit': True
        })

        try:
            if self.shortgiris==1 or self.longgiris==1:
                self.sayici_giris_control += 1
                if self.sayici_giris_control ==500:
                    print(symbol,timeframe,self.sayici_giris_control)
                    self.longgiris=0
                    self.shortgiris=0


            else:
                bars = exchange.fetch_ohlcv(symbol, timeframe=timeframe, since=None, limit=200)
                df = pd.DataFrame(bars, columns=["timestamp", "open", "high", "low", "close", "volume"])

                macddf = df.ta.macd(close='close', fast=12, slow=26, signal=9, append=True)

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

                    if self.kesisimmovaverage == 1 and self.kesisimmacdsayac == 1:
                        if self.macdlast > 0:
                            print('long gir')
                            tele.telegram_bot('long gir-macdmov_strategy')
                            tele.telegram_bot(symbol)
                            #self.kesisimmovaverage = 0
                            #self.kesisimmacdsayac = 0
                            self.longgiris += 1
                            print(symbol, longgiris,"alis_sonrasi")
                            time.sleep(10)
                        else:
                            print("short_gir")

                            tele.telegram_bot("short_gir-macdmov_strategy")
                            tele.telegram_bot(symbol)

                            #self.kesisimmovaverage = 0
                            #self.kesisimmacdsayac = 0
                            self.shortgiris += 1
                            print(symbol,shortgiris,"alis_sonrasi")
                            time.sleep(10)

        except ccxt.BaseError as Error:
            print("[ERROR] ", Error)


coin2=Macdema('ETHUSDT',"1h")
coin1=Macdema('BTCUSDT',"1h")
coin3=Macdema('ATOMUSDT',"1h")
coin4=Macdema('EOSUSDT',"1h")
coin5=Macdema('LITUSDT',"1h")
coin6=Macdema('ICPUSDT',"1h")
coin7=Macdema('CRVUSDT',"1h")
coin8=Macdema('THETAUSDT',"1h")
coin9=Macdema('XRPUSDT',"1h")
coin10=Macdema('RUNEUSDT',"1h")
coin11=Macdema('ARUSDT',"1h")
coin12=Macdema('DOTUSDT',"1h")
coin13=Macdema('ETCUSDT',"1h")
coin14=Macdema('ALGOUSDT',"1h")
coin15=Macdema('TRXUSDT',"1h")
coin16=Macdema('LRCUSDT',"1h")
coin17=Macdema('SANDUSDT',"1h")

coin2a=Macdema('ETHUSDT',"1m")
coin1a=Macdema('BTCUSDT',"1m")
coin3a=Macdema('ATOMUSDT',"1m")
coin4a=Macdema('EOSUSDT',"1m")
coin5a=Macdema('LITUSDT',"1m")
coin6a=Macdema('ICPUSDT',"1m")
coin7a=Macdema('CRVUSDT',"1m")
coin8a=Macdema('THETAUSDT',"1m")
coin9a=Macdema('XRPUSDT',"1m")
coin10a=Macdema('RUNEUSDT',"1m")
coin11a=Macdema('ARUSDT',"1m")
coin12a=Macdema('DOTUSDT',"1m")
coin13a=Macdema('ETCUSDT',"1m")
coin14a=Macdema('ALGOUSDT',"1m")
coin15a=Macdema('TRXUSDT',"1m")
coin16a=Macdema('LRCUSDT',"1m")
coin17a=Macdema('SANDUSDT',"1m")


while True:

    coin2.dfall('ETHUSDT',"1h")
    coin1.dfall('BTCUSDT',"1h")
    coin3.dfall('ATOMUSDT',"1h")
    coin4.dfall('EOSUSDT',"1h")
    coin5.dfall('LITUSDT',"1h")
    coin6.dfall('ICPUSDT',"1h")
    coin7.dfall('CRVUSDT',"1h")
    coin8.dfall('THETAUSDT',"1h")
    coin9.dfall('XRPUSDT',"1h")
    coin10.dfall('RUNEUSDT',"1h")
    coin11.dfall('ARUSDT',"1h")
    coin12.dfall('DOTUSDT',"1h")
    coin13.dfall('ETCUSDT',"1h")
    coin14.dfall('ALGOUSDT',"1h")
    coin15.dfall('TRXUSDT',"1h")
    coin16.dfall('LRCUSDT',"1h")
    coin17.dfall('SANDUSDT',"1h")

    coin2a.dfall('ETHUSDT', "1m")
    coin1a.dfall('BTCUSDT', "1m")
    coin3a.dfall('ATOMUSDT', "1m")
    coin4a.dfall('EOSUSDT', "1m")
    coin5a.dfall('LITUSDT', "1m")
    coin6a.dfall('ICPUSDT', "1m")
    coin7a.dfall('CRVUSDT', "1m")
    coin8a.dfall('THETAUSDT', "1m")
    coin9a.dfall('XRPUSDT', "1m")
    coin10a.dfall('RUNEUSDT', "1m")
    coin11a.dfall('ARUSDT', "1m")
    coin12a.dfall('DOTUSDT', "1m")
    coin13a.dfall('ETCUSDT', "1m")
    coin14a.dfall('ALGOUSDT', "1m")
    coin15a.dfall('TRXUSDT', "1m")
    coin16a.dfall('LRCUSDT', "1m")
    coin17a.dfall('SANDUSDT', "1m")

    coin2a.addspread(1,1,1,2,1,3,1,4,1,5,1,6)


    coin1a.addspread(2,1,2,2,2,3,2,4,2,5,2,6)
    time.sleep(5)

    coin3a.addspread(3,1,3,2,3,3,3,4,3,5,3,6)
    time.sleep(5)

    coin4a.addspread(4,1,4,2,4,3,4,4,4,5,4,6)
    time.sleep(5)

    coin5a.addspread(5, 1, 5, 2,5,3,5,4,5,5,5,6)
    time.sleep(5)

    coin6a.addspread(6, 1, 6, 2,6,3,6,4,6,5,6,6)
    time.sleep(5)

    coin7a.addspread(7, 1, 7, 2,7,3,7,4,7,5,7,6)
    time.sleep(5)

    coin8a.addspread(8, 1, 8, 2,8,3,8,4,8,5,8,6)
    time.sleep(5)

    coin9a.addspread(9, 1, 9, 2,9,3,9,4,9,5,9,6)
    time.sleep(5)

    coin10a.addspread(10, 1, 10, 2,10,3,10,4,10,5,10,6)
    time.sleep(5)

    coin11a.addspread(11, 1, 11, 2,11,3,11,4,11,5,11,6)
    time.sleep(5)

    coin12a.addspread(12, 1, 12, 2,12,3,12,4,12,5,12,6)





    time.sleep(25)




