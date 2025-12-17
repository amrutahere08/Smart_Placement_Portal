from app import app
from db import get_db

def verify_data():
    with app.app_context():
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        print("=== DATA VERIFICATION ===")
        
        # 1. Students
        cursor.execute("SELECT id, email FROM studentlogin")
        students = cursor.fetchall()
        print(f"Students found: {len(students)}")
        for s in students:
            print(f" - ID {s['id']}: {s['email']}")

        # 2. Companies
        cursor.execute("SELECT id, name FROM company")
        companies = cursor.fetchall()
        print(f"Companies found: {len(companies)}")
        for c in companies:
            print(f" - ID {c['id']}: {c['name']}")
        
        # 3. Applications
        cursor.execute("SELECT * FROM applications")
        apps = cursor.fetchall()
        print(f"Applications found: {len(apps)}")
        for a in apps:
            print(f" - App {a['id']}: Student {a['student_id']} -> Company {a['company_id']} ({a['status']})")
            
        if not apps:
            print("!!! WARNING: APPLICATIONS TABLE IS EMPTY !!!")

if __name__ == "__main__":
    verify_data()
