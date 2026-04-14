<<<<<<< HEAD
import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT,
password TEXT,
streak INTEGER DEFAULT 0,
last_quiz_date TEXT
)
""")

conn.commit()
=======
import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT,
password TEXT,
streak INTEGER DEFAULT 0,
last_quiz_date TEXT
)
""")

conn.commit()
>>>>>>> 4b72cdccd7641943b955334ed39ab7a7af142874
conn.close()