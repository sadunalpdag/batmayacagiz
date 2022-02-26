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
import array_ekle
import bband as bband

highmat = array_ekle.highmat
Openmat = array_ekle.Openmat
lowmat =  array_ekle.lowmat
matris =  array_ekle.matris
bbandhigh=[]
bbandlow=[]
bbandmid=[]


matrisn1 =matris[1:]
matrisn2 =matris[2:]
matrisn3 =matris[3:]
matrisn4 =matris[4:]
matrisn5 =matris[5:]
matrisn6 =matris[6:]
matrisn7 =matris[7:]
matrisn8 =matris[8:]
matrisn9 =matris[9:]



print(len(matrisn1))
print(len(matrisn2))
print(len(matrisn3))
print(len(matrisn4))
n=int(len(matrisn9))

fark=[]
fark1=[]
fark2=[]
fark3=[]
fark4=[]
fark5=[]
fark6=[]
fark7=[]


for i  in range(0,n):

    fark11=((matrisn1[i]/matrisn2[i])-1)
    fark21=((matrisn1[i]/matrisn3[i])-1)
    fark31 = ((matrisn1[i] / matrisn4[i]) - 1)
    fark41 = ((matrisn1[i] / matrisn5[i]) - 1)
    fark51 = ((matrisn1[i] / matrisn6[i]) - 1)
    fark61 = ((matrisn1[i] / matrisn7[i]) - 1)
    fark71 = ((matrisn1[i] / matrisn8[i]) - 1)
    fark81 = ((matrisn1[i] / matrisn9[i]) - 1)

    fark.append(fark11)
    fark1.append(fark21)
    fark2.append(fark31)
    fark3.append(fark41)
    fark4.append(fark51)
    fark5.append(fark61)
    fark6.append(fark71)
    fark7.append(fark81)

largest1 = fark[0]
smallest1 = fark[0]
for i  in range(0,n):
    if fark[i]>largest1:
        largest1 = fark[i]
    if fark[i]<smallest1:
        smallest1 = fark[i]
print(largest1)
print(smallest1)

largest2 = fark1[0]
smallest2 = fark1[0]
for i  in range(0,n):
    if fark1[i]>largest2:
        largest2 = fark1[i]
    if fark1[i]<smallest2:
        smallest2 = fark1[i]
print(largest2)
print(smallest2)

largest3 = fark2[0]
smallest3 = fark2[0]
for i  in range(0,n):
    if fark2[i]>largest3:
        largest3 = fark2[i]
    if fark2[i]<smallest3:
        smallest3 = fark2[i]
print(largest3)
print(smallest3)

largest4 = fark3[0]
smallest4 = fark3[0]
for i  in range(0,n):
    if fark3[i]>largest4:
        largest4 = fark3[i]
    if fark3[i]<smallest4:
        smallest4 = fark3[i]
print(largest4)
print(smallest4)

largest5 = fark4[0]
smallest5 = fark4[0]
for i  in range(0,n):
    if fark4[i]>largest5:
        largest5 = fark4[i]
    if fark4[i]<smallest5:
        smallest5 = fark4[i]
print(largest5)
print(smallest5)

largest6 = fark5[0]
smallest6 = fark5[0]
for i  in range(0,n):
    if fark5[i]>largest6:
        largest6 = fark5[i]
    if fark4[i]<smallest6:
        smallest6 = fark5[i]
print(largest6)
print(smallest6)

largest7 = fark6[0]
smallest7 = fark6[0]
for i  in range(0,n):
    if fark6[i]>largest7:
        largest7 = fark6[i]
    if fark6[i]<smallest7:
        smallest7 = fark6[i]
print(largest7)
print(smallest7)

largest8 = fark7[0]
smallest8 = fark7[0]
for i  in range(0,n):
    if fark7[i]>largest8:
        largest8 = fark7[i]
    if fark7[i]<smallest8:
        smallest8 = fark7[i]
print(largest8)
print(smallest8)





print(fark)
print(fark1)
print(fark2)
print(fark3)
print(fark4)
print(fark5)
print(fark6)
print(fark7)








print(matrisn1)
print(matrisn2)
print(matrisn3)
print(matrisn4)

lenght_rsi = 0
rsi_current = 0
rsi_son_float = 0
countrsi = 0
series = range(49)
print('working')

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
    fark122 = pd.DataFrame(fark1,columns=['fark1'])
    fark123 = pd.DataFrame(fark2, columns=['fark2'])
    fark124 = pd.DataFrame(fark3, columns=['fark3'])
    fark125 = pd.DataFrame(fark4, columns=['fark4'])
    fark126 = pd.DataFrame(fark5, columns=['fark5'])
    fark127 = pd.DataFrame(fark6, columns=['fark6'])
    fark128 = pd.DataFrame(fark7, columns=['fark7'])





    stresult=stfunc.supertrend(data4,data3,data,x11)

    print('stperc',stresult[0])
    print('stresul',stresult[1])


    supertrend_mat=stresult[2]
    adx_mat =stresult[3]
    #tele.telegram_bot('Working')

    rsiresult = rsi.rsi(data,lenght_rsi)

    print('rsilast', rsiresult)

    inv_fisher =fisher.inv_fisher(data4,data3,lenght_rsi)

    print('invfisher',inv_fisher)



    bbandresult = bband.bbands_result(data)
    bbandlow_mat = bbandresult[0]
    bbandmid_mat = bbandresult[1]
    bbandhigh_mat = bbandresult[2]


    print(bbandresult)

    movingaverageresult = mov.movingaverage(data, x11)

    print('movaverage perc',movingaverageresult[0])
    print('moving average',movingaverageresult[1])
    moving_50=movingaverageresult[2]
    moving_100=movingaverageresult[3]
    moving_200=movingaverageresult[4]

    macd1 = ta.rsi(data['close'], length=14)
    # print(macd1)
    macd2 = ta.rsi(data['close'], length=28)
    macd3 = ta.macd(data['close'], fast=14, slow=28)



    # print(macd3 )
    data2 = pd.concat([data, macd1, macd2,moving_200,adx_mat,moving_100,moving_50, macd3,data3,data4,supertrend_mat,bbandlow_mat,bbandhigh_mat,bbandmid_mat,fark122,fark123,fark124,fark125,fark126,fark127,fark128], axis=1,)
    data3= data2.applymap("{0:.6f}".format)

    data3.to_csv(r'C:\Users\rage\PycharmProjects\batmayacagiz\export_dataframe.csv', index=False, header=True)





    print(data2)



    if x1 > y1:
        print('yukseliyor')


    else:
        print('dusuyor')


while True:
    price()
