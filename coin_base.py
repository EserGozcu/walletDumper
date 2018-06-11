from coinbase.wallet.client import Client
import json
import urllib
import time
import sqlite3
import datetime
from pathlib import Path
import os





sqlite_file = '/Users/esergozcu/Documents/PycharmProjects/coinbase/my_db.sqlite'
table_name = 'wallet_info'
id_field = 'id_field' # name of the ID column
date_col = 'date_col' # name of the date column
field_type = 'TEXT'  # column data type
value_col = 'value_col'
value_col_type = 'INTEGER'

id_field_number = 1


my_file = Path("/Users/esergozcu/Documents/PycharmProjects/coinbase/my_db.sqlite") #check if sqlite file there, then delete it for a clean start
if my_file.is_file():
    os.remove('/Users/esergozcu/Documents/PycharmProjects/coinbase/my_db.sqlite')

# Connecting to the database file
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()





# Creating a new SQLite table with 1 column and adding one more column

c.execute('CREATE TABLE {tn} ({fn} {ft} PRIMARY KEY)'\
          .format(tn=table_name, fn=id_field, ft=field_type))
# A) Adding a new column to save date insert a row with the current date
# in the following format: YYYY-MM-DD
# e.g., 2014-03-06
c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}'"\
          .format(tn=table_name, cn=date_col))


c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}'"\
          .format(tn=table_name, cn=value_col))



client = Client("<access keyid>","<access secretid>")
balance_list = list()
accounts = client.get_accounts()

for account in accounts.data:
  balance = account.balance.amount
  balance = float(balance)
  balance_list.append(balance) #this is to put account amounts into list for all different wallets


#print (balance_list)


url_ltc = ['https://api.coinbase.com/v2/prices/LTC-SEK/sell']
url_eth = ['https://api.coinbase.com/v2/prices/ETH-SEK/sell']
url_btc = ['https://api.coinbase.com/v2/prices/BTC-SEK/sell']



while 1<2:
    for url in url_ltc:
        url = urllib.request.urlopen(url_ltc[0])
        result = json.load(url)  # result is now a dict
        current_price = result['data']['amount']
        current_price = float(current_price)
        total_value_litecoin = current_price * balance_list[1]
        #print total_value_litecoin
        #time.sleep(10)

    for url in url_eth:
        url = urllib.request.urlopen(url_eth[0])
        result = json.load(url)
        current_price = result['data']['amount']
        current_price = float(current_price)
        total_value_eth = current_price * balance_list[2]
        #print (total_value_ethtable_name)

    for url in url_btc:
        url = urllib.request.urlopen(url_btc[0])
        result = json.load(url)
        current_price = result['data']['amount']
        current_price = float(current_price)
        total_value_btc = current_price * balance_list[3]
        #print (total_value_eth)

    wallet_value = (total_value_litecoin + total_value_eth + total_value_btc)
    c.execute("insert into wallet_info (id_field, date_col,value_col) values (?,CURRENT_TIMESTAMP,?)", (id_field_number, wallet_value))
    conn.commit()
    id_field_number = id_field_number + 1
    time.sleep(10)



