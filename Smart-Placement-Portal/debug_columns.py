from app import app
from db import get_db

def debug_columns():
    with app.app_context():
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        print("Checking Keys...")
        
        try:
            cursor.execute("SELECT * FROM company LIMIT 1")
            res = cursor.fetchone()
            if res:
                print("COMPANY Check:", list(res.keys()))
            else:
                # If empty, describe
                cursor.execute("DESCRIBE company")
                print("COMPANY DESC:", [r['Field'] for r in cursor.fetchall()])
                
            cursor.execute("SELECT * FROM applications LIMIT 1")
            res = cursor.fetchone()
            if res:
                print("APPLICATIONS Check:", list(res.keys()))
            else:
                cursor.execute("DESCRIBE applications")
                print("APPLICATIONS DESC:", [r['Field'] for r in cursor.fetchall()])
                
        except Exception as e:
            print(e)

if __name__ == "__main__":
    debug_columns()
