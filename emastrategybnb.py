import ccxt,config
import pandas as pd
from ta.trend import EMAIndicator
import time
import send_msg as tele
import os, psutil
alinacak_miktar = 0

kesisim = False
longPozisyonda = False
shortPozisyonda = False
pozisyondami = False

# API CONNECT
exchange = ccxt.binance({
    "apiKey": config.apiKey,
    "secret": config.secretKey,

    'options': {
        'defaultType': 'future'
    },
    'enableRateLimit': True
})
sayicilong = 0
sayicishort = 0
sayicilongbnb = 0
sayicishortbnb = 0
sayicilongeth = 0
sayicishorteth = 0



while True:
    time.sleep(3)
    try:


        process = psutil.Process(os.getpid())
        print(process.memory_info().rss)  # in bytes

        balance = exchange.fetch_balance()
        free_balance = exchange.fetch_free_balance()
        positions = balance['info']['positions']

        current_positions = [position for position in positions if
                             float(position['positionAmt']) != 0 and position['symbol'] == 'BNBUSDT']
        position_bilgi = pd.DataFrame(current_positions,
                                      columns=["symbol", "entryPrice", "unrealizedProfit", "isolatedWallet",
                                               "positionAmt", "positionSide"])



        # LOAD BARS1
        bars = exchange.fetch_ohlcv('BNBUSDT', timeframe='1h', since=None, limit=100)
        df = pd.DataFrame(bars, columns=["timestamp", "open", "high", "low", "close", "volume"])

        # LOAD SLOW EMA
        slowEma = EMAIndicator(df["close"], float(12))
        df["Slow Ema"] = slowEma.ema_indicator()
        print( df["Slow Ema"])

        # LOAD FAST EMA
        FastEma = EMAIndicator(df["close"], float(26))
        df["Fast Ema"] = FastEma.ema_indicator()
        print(df["Fast Ema"])

        if (df["Fast Ema"][len(df.index) - 3] < df["Slow Ema"][len(df.index) - 3] and df["Fast Ema"][
            len(df.index) - 2] > df["Slow Ema"][len(df.index) - 2]) or (
                df["Fast Ema"][len(df.index) - 3] > df["Slow Ema"][len(df.index) - 3] and df["Fast Ema"][
            len(df.index) - 2] < df["Slow Ema"][len(df.index) - 2]):
            kesisim = True
        else:
            kesisim = False

        if sayicilongbnb ==0:
            # BULL EVENT
            if kesisim and df["Fast Ema"][len(df.index) - 2] > df["Slow Ema"][
                len(df.index) - 2]:
                print ('long gir')
                sayicilongbnb += 1
                sayicishortbnb =0
                tele.telegram_bot("long_gir_bnb")


        if sayicishortbnb == 0:
            # BEAR EVENT
            if kesisim and df["Fast Ema"][len(df.index) - 2] < df["Slow Ema"][
                len(df.index) - 2]:
                print('short_gir')
                sayicilongbnb =0
                sayicishortbnb += 1
                tele.telegram_bot("short_gir_bnb")

        current_positions = [position for position in positions if
                            float(position['positionAmt']) != 0 and position['symbol'] == 'ETHUSDT']
        position_bilgi = pd.DataFrame(current_positions,
                                      columns=["symbol", "entryPrice", "unrealizedProfit", "isolatedWallet",
                                               "positionAmt", "positionSide"])

        # LOAD BARS1
        bars = exchange.fetch_ohlcv('ETHUSDT', timeframe='1h', since=None, limit=100)
        df = pd.DataFrame(bars, columns=["timestamp", "open", "high", "low", "close", "volume"])

        # LOAD SLOW EMA
        slowEma = EMAIndicator(df["close"], float(12))
        df["Slow Ema"] = slowEma.ema_indicator()
        print(df["Slow Ema"])

        # LOAD FAST EMA
        FastEma = EMAIndicator(df["close"], float(26))
        df["Fast Ema"] = FastEma.ema_indicator()
        print(df["Fast Ema"])

        if (df["Fast Ema"][len(df.index) - 3] < df["Slow Ema"][len(df.index) - 3] and df["Fast Ema"][
            len(df.index) - 2] > df["Slow Ema"][len(df.index) - 2]) or (
                df["Fast Ema"][len(df.index) - 3] > df["Slow Ema"][len(df.index) - 3] and df["Fast Ema"][
            len(df.index) - 2] < df["Slow Ema"][len(df.index) - 2]):
            kesisim = True
        else:
            kesisim = False

        if sayicilongeth == 0:
            # BULL EVENT
            if kesisim and df["Fast Ema"][len(df.index) - 2] > df["Slow Ema"][
                len(df.index) - 2]:
                print('long gir')
                sayicilongeth += 1
                sayicishorteth = 0
                tele.telegram_bot("long_gireth")

        if sayicishorteth == 0:
            # BEAR EVENT
            if kesisim and df["Fast Ema"][len(df.index) - 2] < df["Slow Ema"][
                len(df.index) - 2]:
                print('short_gir')
                sayicilongeth = 0
                sayicishorteth += 1
                tele.telegram_bot("short_gir_eth")

        balance = exchange.fetch_balance()
        free_balance = exchange.fetch_free_balance()
        positions = balance['info']['positions']

        current_positions = [position for position in positions if
                             float(position['positionAmt']) != 0 and position['symbol'] == 'BTCUSDT']
        position_bilgi = pd.DataFrame(current_positions,
                                      columns=["symbol", "entryPrice", "unrealizedProfit", "isolatedWallet",
                                               "positionAmt", "positionSide"])

        # LOAD BARS1
        bars = exchange.fetch_ohlcv('BTCUSDT', timeframe='1h', since=None, limit=100)
        df = pd.DataFrame(bars, columns=["timestamp", "open", "high", "low", "close", "volume"])

        # LOAD SLOW EMA
        slowEma = EMAIndicator(df["close"], float(12))
        df["Slow Ema"] = slowEma.ema_indicator()
        print(df["Slow Ema"])

        # LOAD FAST EMA
        FastEma = EMAIndicator(df["close"], float(26))
        df["Fast Ema"] = FastEma.ema_indicator()
        print(df["Fast Ema"])

        if (df["Fast Ema"][len(df.index) - 3] < df["Slow Ema"][len(df.index) - 3] and df["Fast Ema"][
            len(df.index) - 2] > df["Slow Ema"][len(df.index) - 2]) or (
                df["Fast Ema"][len(df.index) - 3] > df["Slow Ema"][len(df.index) - 3] and df["Fast Ema"][
            len(df.index) - 2] < df["Slow Ema"][len(df.index) - 2]):
            kesisim = True
        else:
            kesisim = False

        if sayicilong == 0:
            # BULL EVENT
            if kesisim and df["Fast Ema"][len(df.index) - 2] > df["Slow Ema"][
                len(df.index) - 2]:
                print('long gir')
                sayicilong += 1
                sayicishort = 0
                tele.telegram_bot("long_gir")

        if sayicishort == 0:
            # BEAR EVENT
            if kesisim and df["Fast Ema"][len(df.index) - 2] < df["Slow Ema"][
                len(df.index) - 2]:
                print('short_gir')
                sayicilong = 0
                sayicishort += 1
                tele.telegram_bot("short_gir")



    except ccxt.BaseError as Error:
        print("[ERROR] ", Error)
        continue