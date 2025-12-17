from app import app
from db import get_db

def debug_create():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        
        try:
            print("--- APPLICATIONS ---")
            cursor.execute("SHOW CREATE TABLE applications")
            res = cursor.fetchone()
            print(res) # Format: ('applications', 'CREATE TABLE ...')
            
            print("\n--- COMPANY ---")
            cursor.execute("SHOW CREATE TABLE company")
            res = cursor.fetchone()
            print(res)
        except Exception as e:
            print(e)

if __name__ == "__main__":
    debug_create()
