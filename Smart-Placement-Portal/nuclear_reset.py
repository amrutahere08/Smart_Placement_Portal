from app import app
from db import get_db

def nuclear_reset():
    with app.app_context():
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        print("=== NUCLEAR RESET & SEED ===")
        
        # 1. DROP TABLE
        try:
            cursor.execute("DROP TABLE IF EXISTS applications")
            print("Dropped table 'applications'.")
        except Exception as e:
            print(f"Drop failed: {e}")

        # 2. CREATE TABLE
        create_sql = """
        CREATE TABLE applications (
            id INT AUTO_INCREMENT PRIMARY KEY,
            student_id INT,
            company_id INT,
            status VARCHAR(50) DEFAULT 'Applied',
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            interview_date DATETIME DEFAULT NULL,
            resume VARCHAR(255) DEFAULT NULL,
            FOREIGN KEY (student_id) REFERENCES studentlogin(id) ON DELETE CASCADE,
            FOREIGN KEY (company_id) REFERENCES company(id) ON DELETE CASCADE
        )
        """
        try:
            cursor.execute(create_sql)
            print("Created table 'applications' (clean schema).")
        except Exception as e:
            print(f"Create failed: {e}")
            return

        # 3. ENSURE COMPANIES
        # (Name, Role, Date)
        companies = [
            ("Innovate Corp", "Developer", "2025-02-01"),
            ("Global Systems", "Analyst", "2025-02-10"),
            ("Infosys", "System Engineer", "2025-12-12"),
            ("TCS", "Digital Profile", "2025-12-15"),
            ("Amazon SDE", "SDE-1", "2024-03-10"),
            ("Oracle Dev", "Server Developer", "2024-04-15")
        ]
        
        cid_map = {}
        for name, role, date in companies:
            # Check exist (fuzzy for existing ones)
            cursor.execute("SELECT id FROM company WHERE name LIKE %s", (name + '%',))
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

        # 4. SEED APPLICATIONS FOR ALL STUDENTS
        cursor.execute("SELECT id FROM studentlogin")
        students = cursor.fetchall()
        
        if not students:
            print("WARNING: No students found to seed!")
        
        for s in students:
            uid = s['id']
            
            # Helper to insert
            def add_app(c_key, status, int_date=None):
                if c_key not in cid_map: return
                cid = cid_map[c_key]
                sql = "INSERT INTO applications (student_id, company_id, status, interview_date, resume) VALUES (%s, %s, %s, %s, 'dummy.pdf')"
                cursor.execute(sql, (uid, cid, status, int_date))
                print(f"   + Added {c_key} ({status})")

            print(f"Seeding Student {uid}...")
            # 1. Innovate (Interview)
            add_app("Innovate Corp", "Interview Scheduled", "2025-12-19 11:00:00")
            # 2. Global (Interview)
            add_app("Global Systems", "Interview Scheduled", "2025-12-20 14:30:00")
            # 3. Infosys (Selected)
            add_app("Infosys", "Selected", "2025-12-12 10:00:00")
            # 4. TCS (Rejected)
            add_app("TCS", "Rejected", "2025-12-15 10:00:00")
            # 5. Amazon (Selected)
            add_app("Amazon SDE", "Selected", "2024-03-10")
            # 6. Oracle (Rejected)
            add_app("Oracle Dev", "Rejected", "2024-04-15")

        db.commit()
        print("=== NUCLEAR SEED COMPLETE ===")

if __name__ == "__main__":
    nuclear_reset()
