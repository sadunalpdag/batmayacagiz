

from binance.client import Client


import functions as func
import functions_signal as func_sig

import time

import key
import send_msg as tele
import schedule
import time
liste_id=['0']
liste_id1 =['0']
sayici = 0

def signal():
    time.sleep(10)
    func_sig.volume_trader()
    #deneme.tweet_coint()
    #print("merhaba")

while True:
    signal()




