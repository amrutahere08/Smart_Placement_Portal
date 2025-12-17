from app import app
from db import get_db

def seed_final_v3():
    with app.app_context():
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        print("=== SEEDING V3 (Minimal Insert + Update) ===")
        
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
            # Delete old
            cursor.execute("DELETE FROM applications WHERE student_id=%s AND company_id=%s", (uid, aid))
            
            # Minimal Insert (Like app.py)
            cursor.execute("INSERT INTO applications (student_id, company_id) VALUES (%s, %s)", (uid, aid))
            
            # Update to Selected + Date
            cursor.execute(
                "UPDATE applications SET status='Selected', interview_date='2024-03-10' WHERE student_id=%s AND company_id=%s",
                (uid, aid)
            )
            print(f" -> Student {uid}: Added Amazon (Selected)")
            
            # --- ORACLE (Rejected) ---
            oid = cid_map["Oracle Dev"]
            # Delete old
            cursor.execute("DELETE FROM applications WHERE student_id=%s AND company_id=%s", (uid, oid))
            
            # Minimal Insert
            cursor.execute("INSERT INTO applications (student_id, company_id) VALUES (%s, %s)", (uid, oid))
            
            # Update to Rejected + Date
            cursor.execute(
                "UPDATE applications SET status='Rejected', interview_date='2024-04-15' WHERE student_id=%s AND company_id=%s",
                (uid, oid)
            )
            print(f" -> Student {uid}: Added Oracle (Rejected)")
            
        db.commit()
        print("=== SUCCESS ===")

if __name__ == "__main__":
    seed_final_v3()
