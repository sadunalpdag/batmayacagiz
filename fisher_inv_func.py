import pandas_ta as ta

import send_msg as tele
inv_fisher_ulasti=0
def inv_fisher(data4,data3,price_coin_now):
    global inv_fisher_ulasti

    fisherdf = ta.fisher( data4['high'], data3['low'], length=10, )

    fisherlast=fisherdf.iloc[-1]


    if inv_fisher_ulasti==0:
        if fisherlast > 0.25 :
            inv_fisher_ulasti=1
            tele.telegram_bot('inverse_fisher_yukarı kırdı')
            tele.telegram_bot(price_coin_now)
        elif fisherlast <-0.25 :
            inv_fisher_ulasti=1
            tele.telegram_bot('inverse_fisher_asagikırdı')

            tele.telegram_bot(price_coin_now)
    elif     fisherlast  < 0.25 and fisherlast >-0.25 :
             inv_fisher_ulasti=0

    return (fisherlast)
