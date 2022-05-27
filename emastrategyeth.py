
from binance.client import Client
import key
import pandas as pd
import gspread




client = Client(api_key=key.Pkey, api_secret=key.Skey)

trades = client.futures_account_trades()
print (trades)
df = pd.DataFrame(trades, columns=['symbol','id','realizedPnl','buyer','time'])

print(df)
df2 =df.groupby(['symbol'])['symbol'].size().sort_values(ascending=False)
print (df2)
x=df[df['realizedPnl']!="0"]
print(x)
df3 =x.groupby(['symbol'])['symbol'].size().sort_values(ascending=False)
print (df3)


#print(df)
#print (trades)

gc =gspread.service_account(filename='credentials.json')

sh = gc.open_by_key('1jRT7SlWoqaEscBFEz9835rsyrh9m1TNR_HfnGpItTHU')
worksheet = sh.sheet1
worksheet.update([df.columns.values.tolist()] + df.values.tolist())

