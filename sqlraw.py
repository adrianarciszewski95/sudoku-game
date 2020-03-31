import sqlite3

# connect with database
con = sqlite3.connect('statistics.db')

# column access by indexes and by name
con.row_factory = sqlite3.Row

# create cursor
cursor = con.cursor()

# create table in database if not exists
cursor.execute("""
    CREATE TABLE IF NOT EXISTS statistics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        level varchar(10) NOT NULL,
        player varchar(25),
        time varchar(10) NOT NULL,
        hints INTEGER
    )""")

# commit changes in database
con.commit()



