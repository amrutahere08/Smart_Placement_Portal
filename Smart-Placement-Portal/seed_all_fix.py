from app import app
from db import get_db

def troubleshoot_and_seed():
    with app.app_context():
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        print("=== DEBUGGING & SEEDING ===")
        
        # 1. Check/Create Companies
        targets = [
            ("Infosys System Engineer", "System Engineer", "2023-08-15"),
            ("Wipro Turbo", "Project Engineer", "2023-09-20")
        ]
        
        cid_map = {}
        for name, role, date in targets:
            cursor.execute("SELECT id FROM company WHERE name = %s", (name,))
            res = cursor.fetchone()
            if res:
                print(f"[OK] Found Company: {name} (ID: {res['id']})")
                cid_map[name] = res['id']
            else:
                print(f"[MISSING] Creating Company: {name}...")
                cursor.execute(
                    "INSERT INTO company (name, det, curdate, tenth, twelth, btech) VALUES (%s, %s, %s, 60, 60, 60)",
                    (name, role, date)
                )
                cid_map[name] = cursor.lastrowid
                print(f" -> Created with ID: {cid_map[name]}")
        
        db.commit()

        # 2. Assign Applications to ALL Students
        cursor.execute("SELECT id, email FROM studentlogin")
        students = cursor.fetchall()
        print(f"Found {len(students)} students.")
        
        for s in students:
            # Infosys -> Selected
            inf_id = cid_map["Infosys System Engineer"]
            cursor.execute("SELECT id FROM applications WHERE student_id=%s AND company_id=%s", (s['id'], inf_id))
            if not cursor.fetchone():
                cursor.execute(
                    "INSERT INTO applications (student_id, company_id, status) VALUES (%s, %s, 'Selected')",
                    (s['id'], inf_id)
                )
                print(f" -> Added 'Selected' (Infosys) for {s['email']}")
            else:
                cursor.execute(
                    "UPDATE applications SET status='Selected' WHERE student_id=%s AND company_id=%s",
                    (s['id'], inf_id)
                 )
                print(f" -> Updated 'Selected' (Infosys) for {s['email']}")

            # Wipro -> Rejected
            wip_id = cid_map["Wipro Turbo"]
            cursor.execute("SELECT id FROM applications WHERE student_id=%s AND company_id=%s", (s['id'], wip_id))
            if not cursor.fetchone():
                cursor.execute(
                    "INSERT INTO applications (student_id, company_id, status) VALUES (%s, %s, 'Rejected')",
                    (s['id'], wip_id)
                )
                print(f" -> Added 'Rejected' (Wipro) for {s['email']}")
            else:
                 cursor.execute(
                    "UPDATE applications SET status='Rejected' WHERE student_id=%s AND company_id=%s",
                    (s['id'], wip_id)
                 )
                 print(f" -> Updated 'Rejected' (Wipro) for {s['email']}")
                 
        db.commit()
        print("=== DONE ===")

if __name__ == "__main__":
    troubleshoot_and_seed()
