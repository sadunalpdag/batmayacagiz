import pandas_ta as ta

import send_msg as tele
import pandas
inv_fisher_ulasti=0
def inv_fisher(data4,data3,lenrsi):
    global inv_fisher_ulasti

    fisherdf = ta.fisher( data4['high'], data3['low'], length=10, )
    print(fisherdf)
    result = fisherdf .fillna(0)



    ser_singleCol2 = result.iloc[:, 0]  # bununla data set içindeki 1. kolonu cekiyorum
    fisherdflast = (ser_singleCol2.iloc[-1])  # bunu ile dataframedeki son syaıyı alıyorum
    print(lenrsi)

    if lenrsi >500000:
        if inv_fisher_ulasti==0:
            if fisherdf > 0.25 :
                inv_fisher_ulasti=1
                tele.telegram_bot('inverse_fisher_yukarı kırdı')

            elif fisherdf <-0.25 :
                inv_fisher_ulasti=1
                tele.telegram_bot('inverse_fisher_asagikırdı')

            elif fisherdf  < 0.25 and fisherlast >-0.25 :
                inv_fisher_ulasti=0
        elif inv_fisher_ulasti < 0.25 and movingaverageresult > -0.25:
            inv_fisher_ulasti = 0
    return (fisherdflast)
