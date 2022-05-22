from binance.client import Client
import key
import time

class Ucus():


    def __init__(self,symbol,matris):
        self.symbol=symbol
        self.matris = []

    def price(self,symbol,matris):
        client = Client(api_key=key.Pkey, api_secret=key.Skey)
        price = client.get_ticker(symbol=symbol)
        coiprice = format(float(price['askPrice']), )
        x11 = float(coiprice)
        matris.append(x11)
        return (matris)
    def maxnumber(self,matris):
        maxnumber = max(matris)
        return (maxnumber)
    def minnumber(self,matris):
        minnumber = min(matris)
        return (minnumber)

coin1=Ucus('SOLUSDT','SOLUSDT')
coin2=Ucus('BTCUSDT','BTCUSDT')
while True:
    x=coin1.symbol
    y= coin1.matris
    print(x)
    print(y)
    m=coin1.price(x,y)
    max_solusdt=coin1.maxnumber(y)
    min_solusdt=coin1.minnumber(y)
    print(max_solusdt)
    print(min_solusdt)

    print (m)


    xbtc= coin2.symbol
    ybtc = coin2.matris
    print(xbtc)
    print(ybtc)
    n = coin2.price(xbtc, ybtc)
    max_btcusdt = coin2.maxnumber(ybtc)
    min_btcusdt = coin2.minnumber(ybtc)
    print(max_btcusdt)
    print(min_btcusdt)

    print(n)

    time.sleep(15)


