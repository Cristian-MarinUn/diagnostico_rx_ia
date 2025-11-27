import sqlite3
import sys

db = sys.argv[1] if len(sys.argv) > 1 else 'db.sqlite3'
try:
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    rows = cur.fetchall()
    for r in rows:
        print(r[0])
except Exception as e:
    print('ERROR:', e)
    sys.exit(1)
