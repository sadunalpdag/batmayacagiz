import pandas_ta as ta

import send_msg as tele
count_supertrend=0
def supertrend(data4,data3,data,price_coin_now):
    global count_supertrend
    st = ta.supertrend(data4['high'], data3['low'], data['close'], length=10, multiplier=4.0, append=True)
    print(st.tail(10))
    ser_singleCol2 = st.iloc[:, 0]  # bununla data set içindeki 1. kolonu cekiyorum
    stlast= (ser_singleCol2.iloc[-1])  # bunu ile dataframedeki son syaıyı alıyorum
    print(stlast)


    supertrendesult=price_coin_now/stlast
    if count_supertrend==0:
        if supertrendesult > 0.995 and movingaverageresult<1 :
            count_supertrend=1
            tele.telegram_bot('supertrend yakın  sell')
        elif supertrendesult > 1.001 and movingaverageresult<1.005 :
            count_supertrend=1
            tele.telegram_bot('supertrend yakın buy')

            tele.telegram_bot(price_coin_now)
    elif     supertrendesult < 0.995 and movingaverageresult>1.005 :
             count_supertrend=0

    return [supertrendesult,stlast]
