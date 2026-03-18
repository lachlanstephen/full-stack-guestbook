import sqlite3

def init_db():
    create_table = """
        CREATE TABLE IF NOT EXISTS entries (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        email TEXT NOT NULL,
                        message TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
    """

    try:
        with sqlite3.connect("guestbook.db") as con:
            cur = con.cursor()
            cur.execute(create_table)
            con.commit()
            print("Tables created successfully!")

    except sqlite3.OperationalError as e:
        print("Failed to create tables: ", e)