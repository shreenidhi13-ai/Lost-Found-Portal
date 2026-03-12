import sqlite3

conn = sqlite3.connect("database.db")
cur = conn.cursor()

# USERS TABLE
cur.execute("""
CREATE TABLE IF NOT EXISTS
 users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT NOT NULL,
email TEXT UNIQUE NOT NULL,
password TEXT NOT NULL,
points INTEGER DEFAULT 0
)
""")

# ITEMS TABLE
cur.execute("""
CREATE TABLE IF NOT EXISTS
 items(
id INTEGER PRIMARY KEY AUTOINCREMENT,
title TEXT NOT NULL,
description TEXT,
location TEXT,
type TEXT,
user_id INTEGER,
FOREIGN KEY(user_id) REFERENCES users(id)
)
""")

# CLAIMS TABLE
cur.execute("""
CREATE TABLE IF NOT EXISTS
 claims(
id INTEGER PRIMARY KEY AUTOINCREMENT,
item_id INTEGER,
user_id INTEGER,
name TEXT,
phone TEXT,
email TEXT,
message TEXT,
FOREIGN KEY(item_id) REFERENCES items(id),
FOREIGN KEY(user_id) REFERENCES users(id)
)
""")

conn.commit()
conn.close()

print("Database created successfully!")
