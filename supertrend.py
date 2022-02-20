from binance.client import Client
import key
import time
import pandas as pd
import pandas_ta as ta
import numpy as np


matris = [100,200,300,500,900,1250]

highmat = [100,200,300,500,900,1250]
lowmat = [100,200,300,500,900,1250]
lenght_rsi = 0
rsi_current = 0
rsi_son_float = 0
countrsi = 0
series = range(50)


def price():
    time.sleep(3)
    global countrsi

    client = Client(api_key=key.Pkey, api_secret=key.Skey)

    price = client.get_ticker(symbol='BTCBUSD')
    coiprice = format(float(price['askPrice']), )
    highprice = format(float(price['highPrice']), )
    lowprice = format(float(price['lowPrice']), )

    x11 = float(coiprice)
    x12 = float(highprice)
    x13 = float(lowprice)

    matris.append(x11)
    highmat.append(x12)
    lowmat.append(x13)

    x = len(matris) - 1
    y = len(matris) - 2

    xfloat = matris[x]
    yfloat = matris[y]

    x1 = float(xfloat)
    y1 = float(yfloat)

    percent = round(float(x1 / y1), 5)
    print(percent)
    lenght_rsi = len(matris)
    print(countrsi)
    data = pd.DataFrame(matris, columns=['close'])
    data4 = pd.DataFrame(highmat, columns=['high'])
    data3 = pd.DataFrame(lowmat, columns=['low'])

    st = ta.supertrend(data4['high'], data3['low'], data['close'], length=10, multiplier=4.0, append=True)
    print(st)
    bands = ta.bbands(data['close'])
    ser_singleCol2 = bands.iloc[:, 2]#bununla data set içindeki 2. kolonu cekiyorum
    print(ser_singleCol2.iloc[-1])# bunu ile dataframedeki son syaıyı alıyorum
    print(ser_singleCol2)
    print(bands)







while True:
    price()
