import ccxt,config
import pandas as pd
from ta.trend import EMAIndicator
from ta.trend import MACD
import time
import send_msg as tele
import pandas_ta as ta

import gspread


kesisimmacdsayac = 0
kesisimmovaverage = 0








def macdmov():
    global kesisimmacdsayac
    global kesisimmovaverage


    exchange = ccxt.binance({
        "apiKey": config.apiKey,
        "secret": config.secretKey,

        'options': {
            'defaultType': 'future'
        },
        'enableRateLimit': True
    })

    try:
        gc = gspread.service_account(filename='credentials.json')

        sh = gc.open_by_key('15IDisjoICpEu6t2ByuRmsjwK8KyEFOuTCCPMgbt1oxo')
        worksheet = sh.sheet1


        worksheet.update_cell(6, 6, kesisimmacdsayac)
        worksheet.update_cell(6, 7, kesisimmovaverage)
        # LOAD BARS1
        bars = exchange.fetch_ohlcv('BTCUSDT', timeframe='1h', since=None, limit=200)
        df = pd.DataFrame(bars, columns=["timestamp", "open", "high", "low", "close", "volume"])

        macddf = df.ta.macd(close='close', fast=12, slow=26, signal=9, append=True)

        x=(macddf.iloc[:, 1])
        macdlast = (x.iloc[-1])
        print(macdlast)
        df["slow macd"] = macddf.iloc[:, 0]

        macd = MACD(df["close"])

        df["macd"] = macd.macd_signal()
        # LOAD SLOW EMA
        slowEma = EMAIndicator(df["close"], float(12))

        df["Slow Ema"] = slowEma.ema_indicator()

        # LOAD FAST EMA
        FastEma = EMAIndicator(df["close"], float(26))
        df["Fast Ema"] = FastEma.ema_indicator()




        if kesisimmacdsayac==0:
            if (df["macd"][len(df.index) - 3] < df["slow macd"][len(df.index) - 3] and df["macd"][
                len(df.index) - 2] > df["slow macd"][len(df.index) - 2]) or (
                    df["macd"][len(df.index) - 3] > df["slow macd"][len(df.index) - 3] and df["macd"][
                len(df.index) - 2] < df["slow macd"][len(df.index) - 2]):

                kesisimmacdsayac += 1
                tele.telegram_bot("macdkesisim")
                print(df["macd"])
                print(df["slow macd"])


        if kesisimmovaverage==0:

            if (df["Fast Ema"][len(df.index) - 3] < df["Slow Ema"][len(df.index) - 3] and df["Fast Ema"][
                len(df.index) - 2] > df["Slow Ema"][len(df.index) - 2]) or (
                    df["Fast Ema"][len(df.index) - 3] > df["Slow Ema"][len(df.index) - 3] and df["Fast Ema"][
                len(df.index) - 2] < df["Slow Ema"][len(df.index) - 2]):

                kesisimmovaverage += 1
                tele.telegram_bot("movkesisim")
                print(df["Slow Ema"])
                print(df["Fast Ema"])


        if kesisimmovaverage == 1 and kesisimmacdsayac == 1:
            if macdlast > 0:
                print('long gir')
                tele.telegram_bot("short_gir")
                kesisimmovaverage = 0
                kesisimmacdsayac = 0
                time.sleep(120)
            else:
                print('long gir')
                tele.telegram_bot("short_gir")
                kesisimmovaverage = 0
                kesisimmacdsayac = 0
                time.sleep(120)

    except ccxt.BaseError as Error:
        print("[ERROR] ", Error)

