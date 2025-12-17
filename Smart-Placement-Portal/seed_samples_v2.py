from app import app
from db import get_db

def seed_samples_v2():
    with app.app_context():
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        print("=== SEEDING SAMPLES V2 ===")
        
        # 1. Check if 'resume' column exists in applications
        has_resume = False
        try:
            cursor.execute("SELECT resume FROM applications LIMIT 1")
            print("Detected 'resume' column in applications.")
            has_resume = True
        except Exception as e:
            print("No 'resume' column detected or error checking:", e)
            has_resume = False

        # 2. Ensure Companies
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
                cursor.execute("INSERT INTO company (name, det, curdate, tenth, twelth, btech) VALUES (%s, %s, %s, 60, 60, 60)", (name, role, date))
                cid_map[name] = cursor.lastrowid
                print(f" -> Created Company: {name}")

        # 3. Insert Applications
        cursor.execute("SELECT id, email FROM studentlogin")
        students = cursor.fetchall()
        
        for s in students:
            uid = s['id']
            
            # Amazon -> Selected
            aid = cid_map["Amazon SDE"]
            cursor.execute("DELETE FROM applications WHERE student_id=%s AND company_id=%s", (uid, aid))
            
            if has_resume:
                 cursor.execute(
                    "INSERT INTO applications (student_id, company_id, status, interview_date, resume) VALUES (%s, %s, 'Selected', '2024-03-10', 'sample.pdf')",
                    (uid, aid)
                )
            else:
                cursor.execute(
                    "INSERT INTO applications (student_id, company_id, status, interview_date) VALUES (%s, %s, 'Selected', '2024-03-10')",
                    (uid, aid)
                )
            print(f" -> [Student {uid}] Assigned Amazon (Selected)")
            
            # Oracle -> Rejected
            oid = cid_map["Oracle Dev"]
            cursor.execute("DELETE FROM applications WHERE student_id=%s AND company_id=%s", (uid, oid))
            
            if has_resume:
                cursor.execute(
                    "INSERT INTO applications (student_id, company_id, status, interview_date, resume) VALUES (%s, %s, 'Rejected', '2024-04-15', 'sample.pdf')", 
                    (uid, oid)
                )
            else:
                cursor.execute(
                    "INSERT INTO applications (student_id, company_id, status, interview_date) VALUES (%s, %s, 'Rejected', '2024-04-15')", 
                    (uid, oid)
                )
            print(f" -> [Student {uid}] Assigned Oracle (Rejected)")
            
        db.commit()
        print("=== COMPLETED ===")

if __name__ == "__main__":
    seed_samples_v2()
