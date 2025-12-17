from app import app
from db import get_db

def debug_keys():
    with app.app_context():
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM applications LIMIT 1")
        res = cursor.fetchone()
        if res:
             print("KEYS found:")
             for k in res.keys():
                 print(k)
        else:
             print("No rows in applications table.")
             cursor.execute("DESCRIBE applications")
             print("DESCRIBE:")
             for r in cursor.fetchall():
                 print(r['Field'])

if __name__ == "__main__":
    debug_keys()
