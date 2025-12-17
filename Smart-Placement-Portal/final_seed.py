from app import app
from db import get_db

def final_seed():
    with app.app_context():
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        print("=== FINAL DATA INJECTION ===")
        
        # 1. Ensure Companies Exist
        targets = [
            ("Google SDE", "SDE-1", "2024-05-15"),
            ("Microsoft IDC", "Software Engineer", "2024-06-20")
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

        # 2. Force Insert/Update for ALL Students
        cursor.execute("SELECT id, email FROM studentlogin")
        students = cursor.fetchall()
        
        for s in students:
            uid = s['id']
            # Google -> Selected
            gid = cid_map["Google SDE"]
            # Delete existing to force insert clean (avoid checking status)
            cursor.execute("DELETE FROM applications WHERE student_id=%s AND company_id=%s", (uid, gid))
            cursor.execute(
                "INSERT INTO applications (student_id, company_id, status, interview_date) VALUES (%s, %s, 'Selected', '2024-05-15')",
                (uid, gid)
            )
            print(f" -> [Student {uid}] Assigned Google (Selected)")
            
            # Microsoft -> Rejected
            mid = cid_map["Microsoft IDC"]
            cursor.execute("DELETE FROM applications WHERE student_id=%s AND company_id=%s", (uid, mid))
            cursor.execute(
                "INSERT INTO applications (student_id, company_id, status, interview_date) VALUES (%s, %s, 'Rejected', '2024-06-20')", 
                (uid, mid)
            )
            print(f" -> [Student {uid}] Assigned Microsoft (Rejected)")
            
        db.commit()
        print("=== SUCCESS: Data Injected properly ===")

if __name__ == "__main__":
    final_seed()
