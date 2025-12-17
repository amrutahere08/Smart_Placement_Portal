from app import app
from db import get_db

def refine_interviews():
    with app.app_context():
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        print("Refining Interview Data...")
        
        # 1. DELETE 'TechStart Solutions' application
        # First get company id
        cursor.execute("SELECT id FROM company WHERE name LIKE 'TechStart%'")
        tech = cursor.fetchone()
        if tech:
            cursor.execute("DELETE FROM applications WHERE company_id = %s", (tech['id'],))
            print(f" -> Deleted applications for TechStart Solutions (ID: {tech['id']})")
            
        # 2. UPDATE 'Innovate Corp' -> 19th Dec 11:00 AM
        cursor.execute("SELECT id FROM company WHERE name LIKE 'Innovate%'")
        inn = cursor.fetchone()
        if inn:
            new_date = "2025-12-19 11:00:00"
            cursor.execute("UPDATE applications SET interview_date = %s WHERE company_id = %s AND status = 'Interview Scheduled'", (new_date, inn['id']))
            print(f" -> Updated Innovate Corp to {new_date}")

        # 3. UPDATE 'Global Systems' -> 20th Dec 02:30 PM
        cursor.execute("SELECT id FROM company WHERE name LIKE 'Global%'")
        glob = cursor.fetchone()
        if glob:
            new_date = "2025-12-20 14:30:00"
            cursor.execute("UPDATE applications SET interview_date = %s WHERE company_id = %s AND status = 'Interview Scheduled'", (new_date, glob['id']))
            print(f" -> Updated Global Systems to {new_date}")
            
        db.commit()
        print("Refinement Complete.")

if __name__ == "__main__":
    refine_interviews()
