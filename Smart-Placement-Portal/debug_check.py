from app import app
from db import get_db

def debug_check():
    with app.app_context():
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        print("=== DEBUG CHECK ===")
        # 1. Check Companies
        cursor.execute("SELECT id, name FROM company WHERE name LIKE 'Infosys%' OR name LIKE 'Wipro%'")
        comps = cursor.fetchall()
        print("Companies:", comps)
        comp_ids = [c['id'] for c in comps]

        if not comp_ids:
            print("ERROR: Companies not found.")
            return

        # 2. Check Applications
        print("\nChecking Applications for these companies:")
        format_str = ','.join(['%s'] * len(comp_ids))
        cursor.execute(f"SELECT * FROM applications WHERE company_id IN ({format_str})", tuple(comp_ids))
        apps = cursor.fetchall()
        
        print(f"Found {len(apps)} applications.")
        for a in apps[:5]:
            print(f" - App ID: {a['id']}, Student: {a['student_id']}, Company: {a['company_id']}, Status: {a['status']}")

        # 3. Check Students
        print("\nChecking Students:")
        cursor.execute("SELECT id, email, fname FROM studentlogin LIMIT 5")
        students = cursor.fetchall()
        for s in students:
            print(f" - Student {s['id']}: {s['email']}")

            # Check specific app for this student
            cursor.execute("SELECT * FROM applications WHERE student_id = %s", (s['id'],))
            s_apps = cursor.fetchall()
            print(f"   -> Has {len(s_apps)} apps.")
            
if __name__ == "__main__":
    debug_check()
