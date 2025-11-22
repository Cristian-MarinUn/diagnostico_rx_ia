import sqlite3
import sys

db = sys.argv[1] if len(sys.argv) > 1 else 'db.sqlite3'
conn = sqlite3.connect(db)
cur = conn.cursor()
cur.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='django_migrations'")
if cur.fetchone()[0] == 0:
    print('django_migrations table not found in', db)
    sys.exit(1)

cur.execute("SELECT id, app, name FROM django_migrations WHERE app='admin'")
rows = cur.fetchall()
if not rows:
    print('No admin migrations found to delete')
else:
    print('Found admin migrations:', rows)
    cur.execute("DELETE FROM django_migrations WHERE app='admin'")
    conn.commit()
    print('Deleted admin migration entries')

conn.close()
