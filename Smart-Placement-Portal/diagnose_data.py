from app import app
from db import get_db

def diagnose():
    with app.app_context():
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        print("=== DIAGNOSING DATA ===")
        
        # 1. Check Company Data
        print("\n--- Company Criteria ---")
        cursor.execute("SELECT id, name, btech FROM company")
        companies = cursor.fetchall()
        for c in companies:
            print(f"ID: {c['id']}, Name: {c['name']}, B.Tech: {c['btech']} (Type: {type(c['btech'])})")

        # 2. Check Student Data
        print("\n--- Student Data ---")
        cursor.execute("SELECT id, fname, cgpa, resume_path FROM studentlogin LIMIT 5")
        students = cursor.fetchall()
        for s in students:
            print(f"ID: {s['id']}, Name: {s['fname']}, CGPA: {s['cgpa']} (Type: {type(s['cgpa'])}), Resume: {s['resume_path']}")

if __name__ == "__main__":
    diagnose()
