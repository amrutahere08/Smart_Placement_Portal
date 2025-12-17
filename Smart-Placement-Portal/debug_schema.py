from app import app
from db import get_db

def check_schema():
    with app.app_context():
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        print("Checking Tables Columns...")
        
        for table in ['company', 'applications', 'studentlogin']:
            print(f"--- {table} ---")
            cursor.execute(f"DESCRIBE {table}")
            cols = cursor.fetchall()
            for c in cols:
                print(f"{c['Field']} | {c['Type']} | Null: {c['Null']} | Default: {c['Default']}")

if __name__ == "__main__":
    check_schema()
