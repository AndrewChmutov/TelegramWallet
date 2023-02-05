import sqlite3
import requests
import json


currencies = ['USD', 'EUR', 'PLN', 'UAH', 'BYN']

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Primary currency is stored to show the exchange rates
# corresponding to some specific currency.
# 
# Source and target is used to store the type of currency
# that the user is going to convert in his bank account
cursor.execute("""CREATE TABLE wallet (user_id text, 
    USD float,
    EUR float,
    PLN float,
    UAH float,
    BYN float 
    )""")




truncated = {}
for currency in currencies:
    truncated[currency] = []
    for cur in currencies:
        if currency == cur:
            continue
        url = f'https://open.er-api.com/v6/latest/{currency}'
        truncated[currency].append((cur, requests.get(url).json()['rates'][cur]))

with open('exrates.json', 'w') as exrates:
    json.dump(truncated, exrates)

# print(response.json()['rates'])