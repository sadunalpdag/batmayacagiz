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

highmat = [40139.91, 39991.6, 39960.0, 40030.68, 40031.97, 39995.13, 39910.62, 39880.93, 39861.08, 39770.0, 39710.4, 39612.24, 39452.03, 39064.04, 38900.0, 38847.94, 38853.64, 38446.35, 38440.72, 38282.29, 38370.83, 38398.2, 38307.58, 38373.82, 38630.31, 38395.6, 38323.97, 38350.0, 38318.2, 38233.0, 38313.32, 38431.9, 38524.11, 38445.0, 38420.32, 38346.93, 38399.27, 38472.18, 38463.17, 38446.56, 38417.14, 38375.99, 38376.0, 38274.4, 38400.28, 38874.01, 38988.8, 38763.11]
Openmat = [40104.17, 39948.65, 39945.31, 39938.79, 40009.76, 39995.12, 39857.15, 39837.2, 39813.91, 39741.6, 39571.79, 39598.84, 39373.72, 39007.87, 38813.47, 38768.16, 38816.32, 38396.43, 38183.52, 38162.59, 38207.09, 38358.04, 38207.65, 38225.29, 38362.47, 38344.6, 38231.52, 38253.68, 38224.45, 38203.37, 38215.37, 38255.51, 38356.0, 38442.27, 38289.9, 38292.14, 38292.39, 38324.66, 38463.17, 38412.43, 38417.14, 38290.77, 38338.46, 38112.86, 38257.92, 38330.49, 38837.05, 38614.54]
lowmat = [39948.65, 39897.95, 39843.46, 39911.28, 39952.35, 39850.0, 39773.24, 39716.04, 39707.35, 39500.0, 39526.69, 39300.8, 38882.35, 38730.13, 38600.0, 38607.82, 38307.21, 38118.0, 38000.0, 38100.49, 38207.09, 38158.5, 38149.09, 38193.09, 38320.34, 38218.01, 38198.16, 38202.58, 38033.75, 38093.44, 38197.5, 38202.32, 38322.6, 38265.86, 38261.47, 38233.0, 38192.8, 38313.9, 38357.58, 38379.0, 38276.04, 38278.91, 38105.37, 38066.02, 38257.92, 38319.99, 38535.63, 38352.75]
matris = [39948.66, 39945.85, 39939.31, 40009.76, 39991.15, 39858.45, 39837.19, 39813.45, 39741.61, 39571.8, 39598.82, 39371.71, 39010.08, 38815.72, 38768.16, 38814.79, 38400.72, 38183.51, 38165.0, 38207.1, 38358.04, 38210.29, 38225.3, 38362.46, 38344.6, 38231.51, 38251.48, 38227.45, 38203.37, 38215.38, 38255.51, 38361.17, 38441.59, 38289.9, 38292.13, 38292.41, 38324.66, 38467.0, 38412.4, 38414.65, 38292.7, 38338.46, 38112.86, 38257.93, 38330.5, 38837.17, 38619.66, 38398.4]

lenght_rsi = 0
rsi_current = 0
rsi_son_float = 0
countrsi = 0
series = range(49)


def price():
    time.sleep(15)
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
    data = pd.DataFrame(matris, columns=['close'])
    data4 = pd.DataFrame(highmat, columns=['high'])
    data3 = pd.DataFrame(lowmat, columns=['low'])




    stresult=stfunc.supertrend(data4,data3,data,x11)

    print('stperc',stresult[0])
    print('stresul',stresult[1])

    rsiresult = rsi.rsi(data, x11,lenght_rsi)

    print('rsilast', rsiresult)


    movingaverageresult = mov.movingaverage(data, x11)

    print('movaverage perc',movingaverageresult[0])
    print('moving average',movingaverageresult[1])

    macd1 = ta.rsi(data['close'], length=14)
    # print(macd1)
    macd2 = ta.rsi(data['close'], length=28)
    macd3 = ta.macd(data['close'], fast=14, slow=28)


    # print(macd3 )
    data2 = pd.concat([data, macd1, macd2, macd3,data3,data4], axis=1)

    ys = np.array(y, dtype=np.float64)
    xs = np.array(series, dtype=int)



    print(data2.tail(10))



    if x1 > y1:
        print('yukseliyor')


    else:
        print('dusuyor')


while True:
    price()
