from app import app
from db import get_db
import mysql.connector

def seed_final_robust():
    with app.app_context():
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        print("=== ROBUST SEEDING (Amazon/Oracle) ===")
        
        # 1. Ensure Companies
        targets = [
            ("Amazon SDE", "SDE-1", "2024-03-10"),
            ("Oracle Dev", "Server Developer", "2024-04-15")
        ]
        
        cid_map = {}
        for name, role, date in targets:
            cursor.execute("SELECT id FROM company WHERE name = %s", (name,))
            res = cursor.fetchone()
            if res:
                cid_map[name] = res['id']
            else:
                cursor.execute(
                    "INSERT INTO company (name, det, curdate, tenth, twelth, btech) VALUES (%s, %s, %s, 60, 60, 60)", 
                    (name, role, date)
                )
                cid_map[name] = cursor.lastrowid
                print(f" -> Created Company: {name}")

        # 2. Insert for All Students
        cursor.execute("SELECT id FROM studentlogin")
        students = cursor.fetchall()
        
        for s in students:
            uid = s['id']
            
            # --- AMAZON (Selected) ---
            aid = cid_map["Amazon SDE"]
            cursor.execute("DELETE FROM applications WHERE student_id=%s AND company_id=%s", (uid, aid))
            
            try:
                # Try Inserting WITH resume
                cursor.execute(
                    "INSERT INTO applications (student_id, company_id, status, interview_date, resume) VALUES (%s, %s, 'Selected', '2024-03-10', 'dummy.pdf')",
                    (uid, aid)
                )
            except mysql.connector.Error as err:
                # If error is about Unknown Column, retry without resume
                print(f"Insertion with resume failed: {err}")
                print("Retrying without resume...")
                cursor.execute(
                    "INSERT INTO applications (student_id, company_id, status, interview_date) VALUES (%s, %s, 'Selected', '2024-03-10')",
                    (uid, aid)
                )
            print(f" -> Student {uid}: Added Amazon (Selected)")
            
            # --- ORACLE (Rejected) ---
            oid = cid_map["Oracle Dev"]
            cursor.execute("DELETE FROM applications WHERE student_id=%s AND company_id=%s", (uid, oid))
            
            try:
                cursor.execute(
                    "INSERT INTO applications (student_id, company_id, status, interview_date, resume) VALUES (%s, %s, 'Rejected', '2024-04-15', 'dummy.pdf')", 
                    (uid, oid)
                )
            except mysql.connector.Error as err:
                print(f"Insertion with resume failed: {err}")
                print("Retrying without resume...")
                cursor.execute(
                    "INSERT INTO applications (student_id, company_id, status, interview_date) VALUES (%s, %s, 'Rejected', '2024-04-15')", 
                    (uid, oid)
                )
            print(f" -> Student {uid}: Added Oracle (Rejected)")
            
        db.commit()
        print("=== SUCCESS ===")

if __name__ == "__main__":
    seed_final_robust()
