from app import app
from db import get_db

def fix_criteria():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        
        print("=== FIXING MISSING CRITERIA ===")
        
        # Update Branch for all companies
        companies = [
            ('Infosys', 'CSE, ISE, ECE'),
            ('TCS', 'All Branches'),
            ('Amazon', 'CSE, ISE'),
            ('Oracle', 'CSE, ISE'),
            ('Innovate Corp', 'CSE, ISE, ECE, MECH'),
            ('Global Systems', 'CSE, ECE')
        ]
        
        for name, branch in companies:
            cursor.execute("UPDATE company SET branch = %s WHERE name = %s", (branch, name))
            print(f"Updated {name} -> {branch}")
            
        # Ensure marks are set (if they were 0 or NULL)
        cursor.execute("UPDATE company SET tenth=60, twelth=60, btech=60 WHERE tenth IS NULL OR tenth=0")
        
        db.commit()
        print("=== SUCCESS: CRITERIA UPDATED ===")

if __name__ == "__main__":
    fix_criteria()
