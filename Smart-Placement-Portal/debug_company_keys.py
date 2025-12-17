from app import app
from db import get_db

def debug_comp_keys():
    with app.app_context():
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM company LIMIT 1")
        res = cursor.fetchone()
        if res:
             print("COMPANY KEYS:")
             for k in res.keys():
                 print(k)

if __name__ == "__main__":
    debug_comp_keys()
