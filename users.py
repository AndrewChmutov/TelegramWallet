import sqlite3

def add_user(user_id: str):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute("""INSERT INTO wallet VALUES (
        ?, 0, 0, 0, 0, 0
    )""", (user_id,))

    conn.commit()
    
