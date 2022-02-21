# importing the module
import csv



# open the file in read mode
filename = open('BTCBUSD-30m-2022-02-205.csv', 'r')

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
Open=[float(y) for y in Open]
print('Openmat =',Open)
Low=[float(z) for z in Low]
print('lowmat =',Low)
Close=[float(m) for m in Close]
print('matris =',Close)

