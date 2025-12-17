from app import app
from db import get_db

def add_more_history():
    with app.app_context():
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        print("Augmenting History...")
        
        # 1. Create Companies if not exist
        companies = [
            ("Accenture Day 1", "Associate", "2024-01-10"),
            ("Capgemini Analyst", "Analyst", "2024-02-20")
        ]
        
        cid_map = {}
        for name, role, date in companies:
            cursor.execute("SELECT id FROM company WHERE name = %s", (name,))
            res = cursor.fetchone()
            if res:
                cid_map[name] = res['id']
            else:
                cursor.execute("INSERT INTO company (name, det, curdate, tenth, twelth, btech) VALUES (%s, %s, %s, 60, 60, 60)", (name, role, date))
                cid_map[name] = cursor.lastrowid
                print(f" -> Created {name}")

        # 2. Assign to ALL Students
        cursor.execute("SELECT id FROM studentlogin")
        students = cursor.fetchall()
        
        for s in students:
            uid = s['id']
            
            # Accenture -> Selected
            acc_id = cid_map["Accenture Day 1"]
            # Check exist
            cursor.execute("SELECT id FROM applications WHERE student_id=%s AND company_id=%s", (uid, acc_id))
            if not cursor.fetchone():
                # Use curdate as interview_date so it shows in the table
                cursor.execute("INSERT INTO applications (student_id, company_id, status, interview_date) VALUES (%s, %s, 'Selected', '2024-01-10')", (uid, acc_id))
                print(f" -> Added Accenture (Selected) for Student {uid}")

            # Capgemini -> Rejected
            cap_id = cid_map["Capgemini Analyst"]
            cursor.execute("SELECT id FROM applications WHERE student_id=%s AND company_id=%s", (uid, cap_id))
            if not cursor.fetchone():
                cursor.execute("INSERT INTO applications (student_id, company_id, status, interview_date) VALUES (%s, %s, 'Rejected', '2024-02-20')", (uid, cap_id))
                print(f" -> Added Capgemini (Rejected) for Student {uid}")
                
        db.commit()
        print("Augmentation Complete.")

if __name__ == "__main__":
    add_more_history()
