from firebase_admin import credentials, firestore
import firebase_admin
import pandas as pd
import send_msg as tele


list1 = []
list2 = []
kimlik = credentials.Certificate("ema_class.json")

app = firebase_admin.initialize_app(kimlik)
db = firestore.client()  # db e baglantı
snapshots = list(db.collection(u'ETHUSDT').get())
df = pd.DataFrame()
for snap in snapshots:

    X = snap.to_dict()
    key = ['position']
    m =([snap.get(k) for k in key])

    key2 =['id']
    n =([snap.get(k) for k in key2])
    list1.append(m)
    list2.append(n)





print(list1)
print(list2)
d = {'situation':list1,'time':list2}
print(d)
df = pd.DataFrame(d, columns=['situation','time'])
print (df)
sellsignal = df.iloc[:, 0]  # bununla data set içindeki 1. kolonu cekiyorum
sellsignallast1 = (sellsignal.iloc[-1])
sellsignallast2 = (sellsignal.iloc[-2])
print(sellsignallast2)
print(sellsignallast1)
if sellsignallast2!=sellsignallast1:
    print ("esit_degil")
    tele.telegram_bot(sellsignallast1)







