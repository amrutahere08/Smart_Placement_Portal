from app import app
from db import get_db

def seed_specific():
    with app.app_context():
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        print("=== SEEDING SPECIFIC REQUEST ===")
        
        # 1. properties
        # Infosys -> Selected -> 2025-12-12
        # TCS -> Rejected -> 2025-12-15
        
        # 2. Ensure Companies
        targets = [
            ("Infosys", "System Engineer", "2025-12-12"),
            ("TCS", "Digital Profile", "2025-12-15")
        ]
        
        cid_map = {}
        for name, role, date in targets:
            # Flexible match
            cursor.execute("SELECT id FROM company WHERE name LIKE %s", (name + '%',))
            res = cursor.fetchone()
            if res:
                cid_map[name] = res['id']
                # Update date to match request? User said "Infosys selected 12/12/2025".
                # Usually Interview Date is what they see in the table.
                # I'll rely on inserting into interview_date.
                print(f"Found {name} (ID: {res['id']})")
            else:
                cursor.execute(
                    "INSERT INTO company (name, det, curdate, tenth, twelth, btech) VALUES (%s, %s, %s, 60, 60, 60)", 
                    (name, role, date) # Using the requested date as drive date too for consistency
                )
                cid_map[name] = cursor.lastrowid
                print(f" -> Created Company: {name}")

        # 3. Find User 'student'
        # Try finding by name or email, else ID 1
        target_uid = 1
        cursor.execute("SELECT id, fname, email FROM studentlogin WHERE fname LIKE '%student%' OR email LIKE '%student%'")
        params = cursor.fetchall()
        
        uids_to_update = []
        if params:
            for p in params:
                print(f"Matches 'student': ID {p['id']} ({p['email']})")
                uids_to_update.append(p['id'])
        else:
            print("No user found matching 'student'. Defaulting to ID 1.")
            uids_to_update.append(1)
            
        # 4. Update Applications
        for uid in uids_to_update:
            # Infosys
            iid = cid_map["Infosys"]
            cursor.execute("DELETE FROM applications WHERE student_id=%s AND company_id=%s", (uid, iid))
            cursor.execute(
                "INSERT INTO applications (student_id, company_id, status, interview_date, resume) VALUES (%s, %s, 'Selected', '2025-12-12 10:00:00', 'dummy.pdf')",
                (uid, iid)
            )
            print(f" -> Student {uid}: Added Infosys (Selected, 2025-12-12)")
            
            # TCS
            tid = cid_map["TCS"]
            cursor.execute("DELETE FROM applications WHERE student_id=%s AND company_id=%s", (uid, tid))
            cursor.execute(
                "INSERT INTO applications (student_id, company_id, status, interview_date, resume) VALUES (%s, %s, 'Rejected', '2025-12-15 10:00:00', 'dummy.pdf')",
                (uid, tid)
            )
            print(f" -> Student {uid}: Added TCS (Rejected, 2025-12-15)")
            
        db.commit()
        print("=== COMPLETED ===")

if __name__ == "__main__":
    seed_specific()
