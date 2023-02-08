import sqlite3
import constants
import exrates

currencies = constants.currencies

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Primary currency is stored to show the exchange rates
# corresponding to some specific currency.
# 
# Source and target is used to store the type of currency
# that the user is going to convert in his bank account
cursor.execute("""CREATE TABLE wallet (user_id text UNIQUE, 
    full_name text,
    username text,
    USD real,
    EUR real,
    PLN real,
    UAH real,
    BYN real 
    )""")

exrates.refresh()