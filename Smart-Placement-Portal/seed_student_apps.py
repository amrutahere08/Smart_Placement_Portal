from app import app
from db import get_db

def seed_student_apps():
    with app.app_context():
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        print("Seeding Student History (Selected/Rejected)...")
        
        # 1. Get Companies
        cursor.execute("SELECT id, name FROM company WHERE name IN ('Infosys System Engineer', 'Wipro Turbo')")
        companies = cursor.fetchall()
        
        comp_map = {c['name']: c['id'] for c in companies}
        
        if 'Infosys System Engineer' not in comp_map or 'Wipro Turbo' not in comp_map:
            print("Run seed_history.py first to create companies!")
            return

        infosys_id = comp_map['Infosys System Engineer']
        wipro_id = comp_map['Wipro Turbo']

        # 2. Get All Students
        cursor.execute("SELECT id, email FROM studentlogin")
        students = cursor.fetchall()
        
        for s in students:
            uid = s['id']
            email = s['email']
            print(f"Processing {email}...")
            
            # Add 'Selected' in Infosys (if not exists)
            cursor.execute("SELECT id FROM applications WHERE student_id=%s AND company_id=%s", (uid, infosys_id))
            if not cursor.fetchone():
                cursor.execute("INSERT INTO applications (student_id, company_id, status) VALUES (%s, %s, 'Selected')", (uid, infosys_id))
                print(f" -> Marked as Selected in Infosys")
                
            # Add 'Rejected' in Wipro (if not exists)
            cursor.execute("SELECT id FROM applications WHERE student_id=%s AND company_id=%s", (uid, wipro_id))
            if not cursor.fetchone():
                cursor.execute("INSERT INTO applications (student_id, company_id, status) VALUES (%s, %s, 'Rejected')", (uid, wipro_id))
                print(f" -> Marked as Rejected in Wipro")

        db.commit()
        print("Seeding Complete! All students now have history.")

if __name__ == "__main__":
    seed_student_apps()
