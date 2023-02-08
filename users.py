import sqlite3

def add_user(user_id: str, full_name: str, username: str):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute('SELECT user_id FROM wallet')
    if cursor.fetchone() is not None:
        return

    cursor.execute("""INSERT INTO wallet VALUES (
        ?, ?, ?, 0, 0, 0, 0, 0
    )""", (user_id, full_name, username))

    conn.commit()
    
def get_balance(user_id: str):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute('SELECT USD, EUR, PLN, UAH, BYN FROM wallet WHERE user_id = ?', (user_id,))

    return cursor.fetchone()


def top_up(user_id: str, currency: str, amount: float):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute(f'UPDATE wallet SET {currency} = {currency} + {amount} WHERE user_id = ?', (user_id,))
    conn.commit()