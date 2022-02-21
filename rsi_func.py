import pandas_ta as ta

import send_msg as tele
countrsi=0
def rsi(data,price_coin_now,lenrsi):
    global countrsi
    macd1 = ta.rsi(data['close'], length=14)
    macd2 = ta.rsi(data['close'], length=28)



    if lenrsi > 50:
        if countrsi == 0:

            if macd1.iloc[-1] < 30:
                print('buy Btc rsi 30 altı')
                countrsi = 1
                tele.telegram_bot(macd1.iloc[-1])
                tele.telegram_bot(macd2.iloc[-1])


            elif macd1.iloc[-1] > 70:
                print('sell btc rsi 70 altı')
                countrsi = 1
                tele.telegram_bot(macd1.iloc[-1])
                tele.telegram_bot(macd2.iloc[-1])


        elif macd1.iloc[-1] in range(30, 69):
            countrsi = 0


    return (macd1.iloc[-1])

