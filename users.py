import sqlite3

def add_user(user_id: str):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute('SELECT user_id FROM wallet')
    if cursor.fetchone() is not None:
        return

    cursor.execute("""INSERT INTO wallet VALUES (
        ?, 0, 0, 0, 0, 0
    )""", (user_id,))

    conn.commit()
    
