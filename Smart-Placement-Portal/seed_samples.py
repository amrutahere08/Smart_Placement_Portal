from app import app
from db import get_db

def seed_samples():
    with app.app_context():
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        print("=== ADDING SAMPLE COMPANIES (Amazon/Oracle) ===")
        
        # 1. Ensure Companies Exist
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

        # 2. Force Insert for ALL Students
        cursor.execute("SELECT id, email FROM studentlogin")
        students = cursor.fetchall()
        
        for s in students:
            uid = s['id']
            # Amazon -> Selected
            aid = cid_map["Amazon SDE"]
            # Clear old if exists to avoid pk error or status check
            cursor.execute("DELETE FROM applications WHERE student_id=%s AND company_id=%s", (uid, aid))
            cursor.execute(
                "INSERT INTO applications (student_id, company_id, status, interview_date) VALUES (%s, %s, 'Selected', '2024-03-10')",
                (uid, aid)
            )
            print(f" -> [Student {uid}] Assigned Amazon (Selected) with Date")
            
            # Oracle -> Rejected
            oid = cid_map["Oracle Dev"]
            cursor.execute("DELETE FROM applications WHERE student_id=%s AND company_id=%s", (uid, oid))
            cursor.execute(
                "INSERT INTO applications (student_id, company_id, status, interview_date) VALUES (%s, %s, 'Rejected', '2024-04-15')", 
                (uid, oid)
            )
            print(f" -> [Student {uid}] Assigned Oracle (Rejected) with Date")
            
        db.commit()
        print("=== SAMPLES ADDED ===")

if __name__ == "__main__":
    seed_samples()
