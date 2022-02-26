import pandas_ta as ta

import send_msg as tele
count_mov_avrage_ulasti=0
def movingaverage(data,price_coin_now):
    global count_mov_avrage_ulasti

    mov50 = ta.sma( data['close'], length=50)
    mov100 = ta.sma(data['close'], length=100)
    mov200 = ta.sma(data['close'], length=200)

    average50=mov50.iloc[-1]

    movingaverageresult=price_coin_now/average50
    if count_mov_avrage_ulasti==0:
        if movingaverageresult > 0.996 and movingaverageresult<1 :
            count_mov_avrage_ulasti=1
            tele.telegram_bot('ortalamaya ulasti')
            tele.telegram_bot(price_coin_now)
        elif movingaverageresult > 1.001 and movingaverageresult<1.005 :
            count_mov_avrage_ulasti=1
            tele.telegram_bot('ortalamaya ulasti')

            tele.telegram_bot(price_coin_now)
    elif     movingaverageresult < 0.995 and movingaverageresult>1.005 :
             count_mov_avrage_ulasti=0

    return [movingaverageresult,average50,mov50,mov100,mov200]
