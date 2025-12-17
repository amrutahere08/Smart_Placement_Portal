from app import app
from db import get_db
import traceback

def test_insert():
    with app.app_context():
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        print("Test Insert Starting...")
        
        try:
            # 1. Get a student
            cursor.execute("SELECT id FROM studentlogin LIMIT 1")
            s = cursor.fetchone()
            if not s:
                print("No students.")
                return
            uid = s['id']
            print(f"Student ID: {uid}")

            # 2. Get a company (Amazon)
            cursor.execute("SELECT id FROM company WHERE name='Amazon SDE'")
            c = cursor.fetchone()
            if not c:
                # Create dummy
                cursor.execute("INSERT INTO company (name, curdate) VALUES ('Test Comp', '2025-01-01')")
                cid = cursor.lastrowid
            else:
                cid = c['id']
            print(f"Company ID: {cid}")
            
            # 3. Try Insert
            print("Attempting INSERT INTO applications...")
            cursor.execute("INSERT INTO applications (student_id, company_id, status, interview_date) VALUES (%s, %s, 'Selected', '2024-03-10')", (uid, cid))
            print("Insert OK.")
            db.commit()
            print("Commit OK.")
            
        except Exception:
            traceback.print_exc()

if __name__ == "__main__":
    test_insert()
