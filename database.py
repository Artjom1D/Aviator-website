import sqlite3

con = sqlite3.connect('data.db')
cur = con.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS user(id INTEGER PRIMARY KEY, email TEXT NOT NULL, password TEXT NOT NULL, username TEXT NOT NULL, score_shishka INTEGER, FOREIGN KEY(score_shishka) REFERENCES score(ponal))""")
con.commit()
cur.execute("""CREATE TABLE IF NOT EXISTS score(ponal INTEGER PRIMARY KEY, score_shishka INTEGER NOT NULL)""")
con.commit()