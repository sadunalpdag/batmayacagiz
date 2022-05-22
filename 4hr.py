from binance.client import Client
import key
import time
import pandas as pd
import pandas_ta as ta
import send_msg as tele
import numpy as np
from scipy.stats import linregress
import movingaverage as mov
import supertrend_func as stfunc
import rsi_func as rsi
import fisher_inv_func as fisher
import bband as bband
import math

highmat = []
lowmat = []
Openmat = []
matris =[]
SOLUSDT=[]
BTCUSDT=[]
COMPUSDT=[]
ONEUSDT=[]
ZECUSDT=[]
ETHUSDT=[]
SANDUSDT=[]
LRCUSDT=[]
TRXUSDT=[]
ALGOUSDT=[]
ETCUSDT=[]
AVAXUSDT=[]
DOTUSDT=[]
ARUSDT=[]
RUNEUSDT=[]
XRPUSDT=[]
THETAUSDT=[]
CRVUSDT=[]
ICPUSDT=[]


coins= ['SOLUSDT',
        'BTCUSDT',
        'COMPUSDT',
        'ONEUSDT',
        'ZECUSDT',
        'ETHUSDT',
        'SANDUSDT',
        'LRCUSDT',
        'TRXUSDT',
        'ALGOUSDT',
        'ETCUSDT',
        'AVAXUSDT',
        'DOTUSDT',
        'ARUSDT',
        'RUNEUSDT',
        'XRPUSDT',
        'THETAUSDT',
        'CRVUSDT',
        'ICPUSDT']

def price():

    time.sleep(900)
    for coin in coins:


        client = Client(api_key=key.Pkey, api_secret=key.Skey)

        price = client.get_ticker(symbol=coin)
        coiprice = format(float(price['askPrice']), )
        highprice = format(float(price['highPrice']), )
        lowprice = format(float(price['lowPrice']), )

        x11 = float(coiprice)
        x12 = float(highprice)
        x13 = float(lowprice)

        matris.append(x11)
        highmat.append(x12)
        lowmat.append(x13)






while True:
    price()

    print(matris)

    m = [matris[i::19] for i in range(19)]

    print(m)

    sol = m[0]

    print(sol[0])



