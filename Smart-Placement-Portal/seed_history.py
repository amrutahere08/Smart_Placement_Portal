from app import app
from db import get_db
import datetime
import random

def seed_history():
    with app.app_context():
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        print("Seeding Historical Data...")
        
        # 1. Add Past Companies
        past_companies = [
            ("Infosys System Engineer", "System Engineer", "2023-08-15", 60, 60, 65),
            ("Wipro Turbo", "Project Engineer", "2023-09-20", 60, 60, 60),
            ("TCS Digital", "Digital Innovator", "2023-10-05", 70, 70, 75)
        ]
        
        company_ids = []
        for name, role, date, tenth, twelth, btech in past_companies:
            cursor.execute("SELECT id FROM company WHERE name = %s", (name,))
            exist = cursor.fetchone()
            if not exist:
                sql = "INSERT INTO company (name, det, curdate, tenth, twelth, btech) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (name, role, date, tenth, twelth, btech))
                company_ids.append(cursor.lastrowid)
                print(f" -> Added Past Drive: {name} ({date})")
            else:
                company_ids.append(exist['id'])

        # 2. Get Students
        cursor.execute("SELECT id FROM studentlogin")
        students = cursor.fetchall()
        
        if not students:
            print("No students found. Run seed_full_data.py first.")
            return

        # 3. Simulate Applications & Statuses
        statuses = ['Selected', 'Rejected']
        
        for comp_id in company_ids:
            # Pick random 3-5 students for each drive
            applicants = random.sample(students, min(len(students), 4))
            
            for student in applicants:
                user_id = student['id']
                
                # Check if already applied
                cursor.execute("SELECT id FROM applications WHERE student_id=%s AND company_id=%s", (user_id, comp_id))
                if not cursor.fetchone():
                    # Decide status
                    status = random.choice(statuses)
                    
                    # Backdate application to drive date
                    # (Note: 'applied_at' col exists in schema? yes, usually default CURRENT_TIMESTAMP, we can override?)
                    # If applied_at is TIMESTAMP DEFAULT CURRENT_TIMESTAMP, we usually can't update it easily without altering schema or just let it be.
                    # But user asked for 'date', probably interview date or drive date is enough.
                    
                    sql = "INSERT INTO applications (student_id, company_id, status) VALUES (%s, %s, %s)"
                    cursor.execute(sql, (user_id, comp_id, status))
                    print(f" -> Student {user_id} applied to Comp {comp_id} -> {status}")

        db.commit()
        print("Seeding History Complete!")

if __name__ == "__main__":
    seed_history()
