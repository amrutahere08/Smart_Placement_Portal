from app import app
from db import get_db
import mysql.connector

def enrich_data():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        
        print("=== ENRICHING DATA ===")
        
        # 1. Enrich Existing Student (ID 1)
        print("1. Updating Student 1...")
        cursor.execute("""
            UPDATE studentlogin 
            SET lname='Hegde', contact='9876543210', dept='CSE', batch='2025', 
                gender='Female', cgpa=9.2, skills='Python, Java, Git', resume_path='resume_1.pdf'
            WHERE id=1
        """)
        
        # 2. Add New Students
        print("2. Adding New Students...")
        new_students = [
            ('Rahul', 'Sharma', 'rahul@gmail.com', '123', '9876543211', 'ISE', '2025', 'Male', 8.5, 'C++, HTML, CSS'),
            ('Priya', 'Verma', 'priya@gmail.com', '123', '9876543212', 'ECE', '2025', 'Female', 8.9, 'IoT, Embedde C')
        ]
        
        for s in new_students:
            try:
                cursor.execute("""
                    INSERT INTO studentlogin (fname, lname, email, password, contact, dept, batch, gender, cgpa, skills, resume_path)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'dummy_resume.pdf')
                """, s)
                print(f"   - Added {s[0]}")
            except mysql.connector.Error as err:
                print(f"   ! Skipped {s[0]} (likely exists): {err}")

        db.commit()

        # 3. Add Applications for New Students
        print("3. Seeding Applications...")
        
        # Get IDs
        cursor.execute("SELECT id, email FROM studentlogin")
        students = {row[1]: row[0] for row in cursor.fetchall()}
        
        cursor.execute("SELECT id, name FROM company")
        companies = {row[1]: row[0] for row in cursor.fetchall()}
        
        # Mapping: Email -> [(Company, Status)]
        apps_to_add = {
            'rahul@gmail.com': [('Infosys', 'Selected'), ('TCS', 'Applied'), ('Amazon', 'Rejected')],
            'priya@gmail.com': [('Infosys', 'Applied'), ('Oracle', 'Selected'), ('Global Systems', 'Interview Scheduled')]
        }
        
        for email, apps in apps_to_add.items():
            if email in students:
                uid = students[email]
                for cname, status in apps:
                    if cname in companies:
                        cid = companies[cname]
                        # Check exist
                        cursor.execute("SELECT 1 FROM applications WHERE student_id=%s AND company_id=%s", (uid, cid))
                        if not cursor.fetchone():
                            cursor.execute("""
                                INSERT INTO applications (student_id, company_id, status, resume)
                                VALUES (%s, %s, %s, 'dummy.pdf')
                            """, (uid, cid, status))
                            print(f"   - Added app: {email} -> {cname}")

        db.commit()
        print("=== SUCCESS: DATA ENRICHED ===")

if __name__ == "__main__":
    enrich_data()
