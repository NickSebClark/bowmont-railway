import sqlite3

con = sqlite3.connect("train.db")

cur = con.cursor()

cur.execute("CREATE TABLE locomotive(number, description, address)")

