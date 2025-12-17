from app import app
from db import get_db
import mysql.connector

def nuclear_fix_v2():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        
        print("=== NUCLEAR FIX V2 STARTING ===")
        
        try:
            # 1. GLOBAL FOREIGN KEY DISABLE
            print("1. Disabling Foreign Keys...")
            cursor.execute("SET FOREIGN_KEY_CHECKS=0")
            
            # 2. DROP EVERYTHING
            print("2. Dropping Tables...")
            tables = ['applications', 'studentlogin', 'company']
            for t in tables:
                try:
                    cursor.execute(f"DROP TABLE IF EXISTS {t}")
                    print(f"   - Dropped {t}")
                except Exception as e:
                    print(f"   ! Failed to drop {t}: {e}")

            # 3. RECREATE STUDENT
            print("3. Creating Student Table...")
            sql_stu = """CREATE TABLE studentlogin (
                id INT AUTO_INCREMENT PRIMARY KEY,
                fname VARCHAR(100), lname VARCHAR(100), email VARCHAR(100) UNIQUE,
                password VARCHAR(100), contact VARCHAR(20), dept VARCHAR(50),
                batch VARCHAR(10), gender VARCHAR(10), resume_path VARCHAR(255) DEFAULT NULL,
                cgpa FLOAT DEFAULT 0.0, skills TEXT
            )"""
            cursor.execute(sql_stu)
            cursor.execute("INSERT INTO studentlogin (fname, email, password) VALUES ('Student User', 'student@gmail.com', '123')")
            
            # 4. RECREATE COMPANY
            print("4. Creating Company Table...")
            sql_com = """CREATE TABLE company (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100), det VARCHAR(255), curdate VARCHAR(50),
                branch VARCHAR(100), tenth FLOAT DEFAULT 60, twelth FLOAT DEFAULT 60,
                btech FLOAT DEFAULT 60, backlog INT DEFAULT 0
            )"""
            cursor.execute(sql_com)
            
            # 5. RECREATE APPLICATIONS (Plain, no Constraints to avoid 1824 recursion)
            print("5. Creating Applications Table...")
            sql_app = """CREATE TABLE applications (
                id INT AUTO_INCREMENT PRIMARY KEY,
                student_id INT, company_id INT, status VARCHAR(50) DEFAULT 'Applied',
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                interview_date DATETIME DEFAULT NULL, resume VARCHAR(255) DEFAULT NULL
            )"""
            cursor.execute(sql_app)
            
            # 6. SEED DATA
            print("6. Seeding Data...")
            companies = [
                ("Infosys", "System Engineer", "2025-12-12"),
                ("TCS", "Digital Profile", "2025-12-15"),
                ("Amazon", "SDE", "2024-03-10"),
                ("Oracle", "Dev", "2024-04-15"),
                ("Innovate Corp", "Dev", "2025-02-01"),
                ("Global Systems", "Analyst", "2025-02-10")
            ]
            cid_map = {}
            for name, role, date in companies:
                cursor.execute("INSERT INTO company (name, det, curdate) VALUES (%s, %s, %s)", (name, role, date))
                cid_map[name] = cursor.lastrowid

            # Get Student ID
            cursor.execute("SELECT id FROM studentlogin LIMIT 1")
            uid = cursor.fetchone()[0]
            
            # Insert Apps
            def add_app(cname, status, idate):
                if cname in cid_map:
                    cursor.execute("INSERT INTO applications (student_id, company_id, status, interview_date, resume) VALUES (%s, %s, %s, %s, 'dummy.pdf')", (uid, cid_map[cname], status, idate))
            
            add_app("Infosys", "Selected", "2025-12-12 10:00:00")
            add_app("TCS", "Rejected", "2025-12-15 10:00:00")
            add_app("Amazon", "Selected", "2024-03-10")
            add_app("Oracle", "Rejected", "2024-04-15")
            add_app("Innovate Corp", "Interview Scheduled", "2025-12-19")
            add_app("Global Systems", "Interview Scheduled", "2025-12-20")
            
            db.commit()
            print("=== SUCCESS: DB RESTORED ===")
            
        except Exception as e:
            print(f"CRITICAL FAILURE: {e}")
        finally:
            # Re-enable checks
            cursor.execute("SET FOREIGN_KEY_CHECKS=1")

if __name__ == "__main__":
    nuclear_fix_v2()
