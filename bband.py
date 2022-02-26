
import pandas_ta as ta


def bbands_result(data):
    bband_low = ta.bbands(data['close'])

    singleCol0 = bband_low.iloc[:, 0]  # bununla data set içindeki 1. kolonu cekiyorum


    singleCol1 = bband_low.iloc[:, 1]  # bununla data set içindeki 1. kolonu cekiyorum


    singleCol2 = bband_low.iloc[:, 2]  # bununla data set içindeki 1. kolonu cekiyorum





    return (singleCol0,singleCol1,singleCol2)