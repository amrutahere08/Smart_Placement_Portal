from app import app
from db import get_db

def seed_applications():
    with app.app_context():
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        print("Seeding Sample Applications...")
        
        # 1. Get Student ID (assuming 'student' user exists from previous seeds)
        cursor.execute("SELECT id FROM studentlogin WHERE uname = 'student'")
        student = cursor.fetchone()
        
        if not student:
            print("Error: 'student' user not found. Please register or run previous seeds.")
            return

        student_id = student['id']
        print(f" -> Found Student ID: {student_id}")

        # 2. Get Company IDs
        cursor.execute("SELECT id FROM company")
        companies = cursor.fetchall()
        
        if not companies:
            print("Error: No companies found.")
            return

        # 3. Insert specific applications
        # Clear existing first to avoid dupes/errors for this test
        cursor.execute("DELETE FROM applications WHERE student_id = %s", (student_id,))
        
        status_list = ['Applied', 'Selected', 'Rejected', 'Interview Scheduled']
        
        import random
        
        for i, comp in enumerate(companies):
            # diverse statuses
            status = status_list[i % len(status_list)]
            
            sql = "INSERT INTO applications (student_id, company_id, status) VALUES (%s, %s, %s)"
            cursor.execute(sql, (student_id, comp['id'], status))
            print(f" -> Added application for Company ID {comp['id']} with status '{status}'")

        db.commit()
        print("Seeding Complete!")

if __name__ == "__main__":
    seed_applications()
