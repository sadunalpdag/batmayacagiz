# importing the module
import csv
import numpy as np


# open the file in read mode
filename = open('BTCUSDT-1h-2022-01.csv', 'r')

# creating dictreader object
file = csv.DictReader(filename)

# creating empty lists
Opentime = []
Open = []
High= []
Low = []
Close = []
Volume = []
Closetime= []


# iterating over each row and append
# values to empty list
for col in file:
    Opentime.append(col['Opentime'])
    Open.append(col['Open'])
    High.append(col['High'])
    Low.append(col['Low'])
    Close.append(col['Close'])
    Volume.append(col['Volume'])
    Closetime.append(col['Closetime'])

High=[float(x) for x in High]
print('highmat =',High)
Open=[float(x) for x in Open]
print('Openmat =',High)
Low=[float(x) for x in Low]
print('Lowmat =',High)
Close=[float(x) for x in Close]
print('matris =',High)

