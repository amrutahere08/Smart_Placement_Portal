from app import app
from db import get_db
import traceback

def emergency_restore():
    with app.app_context():
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        print("=== EMERGENCY RESTORE ===")
        
        # 1. DROP & CREATE
        try:
            cursor.execute("DROP TABLE IF EXISTS applications")
            print("Dropped old 'applications'.")
        except Exception as e:
            print(e)
            
        sql = """
        CREATE TABLE IF NOT EXISTS applications (
            id INT AUTO_INCREMENT PRIMARY KEY,
            student_id INT NOT NULL,
            company_id INT NOT NULL,
            status VARCHAR(50) DEFAULT 'Applied',
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            interview_date DATETIME DEFAULT NULL,
            resume VARCHAR(255) DEFAULT NULL
        ) Engine=InnoDB;
        """
        try:
            cursor.execute(sql)
            print("Table 'applications' (re)created.")
        except Exception:
            print("Create Failed:")
            traceback.print_exc()
            return

        # 2. SEED DATA
        # Ensure companies exist
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
                print(f" -> Created: {name}")

        # Seed for Student 1 (assuming user is student 1)
        # Actually seed for ALL
        cursor.execute("SELECT id FROM studentlogin")
        students = cursor.fetchall()

        for s in students:
            uid = s['id']
            
            # Helper
            def seed(cname, stat, idate):
                if cname not in cid_map: return
                cid = cid_map[cname]
                # Cleanup
                cursor.execute("DELETE FROM applications WHERE student_id=%s AND company_id=%s", (uid, cid))
                # Insert
                cursor.execute(
                    "INSERT INTO applications (student_id, company_id, status, interview_date, resume) VALUES (%s, %s, %s, %s, 'dummy.pdf')",
                    (uid, cid, stat, idate)
                )
                print(f"   + St{uid}: {cname} -> {stat}")

            seed("Innovate Corp", "Interview Scheduled", "2025-12-19 11:00:00")
            seed("Global Systems", "Interview Scheduled", "2025-12-20 14:30:00")
            seed("Infosys", "Selected", "2025-12-12 10:00:00")
            seed("TCS", "Rejected", "2025-12-15 10:00:00")
            seed("Amazon SDE", "Selected", "2024-03-10")
            seed("Oracle Dev", "Rejected", "2024-04-15")

        db.commit()
        print("=== RESTORE & SEED COMPLETE ===")

if __name__ == "__main__":
    emergency_restore()
