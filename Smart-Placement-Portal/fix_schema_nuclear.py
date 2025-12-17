from app import app
from db import get_db

def fix_schema_nuclear():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        
        print("=== NUCLEAR SCHEMA FIX ===")
        
        # 1. Try modifying existing column
        try:
            print("Attempting to MODIFY resume to DEFAULT NULL...")
            cursor.execute("ALTER TABLE applications MODIFY resume VARCHAR(255) DEFAULT NULL")
            print("Success: Modified existing 'resume' column.")
        except Exception as e:
            print(f"Modify failed ({e}). Assuming column doesn't exist.")
            
            # 2. Try adding column
            try:
                print("Attempting to ADD resume column...")
                cursor.execute("ALTER TABLE applications ADD COLUMN resume VARCHAR(255) DEFAULT NULL")
                print("Success: Added 'resume' column.")
            except Exception as e2:
                print(f"Add failed ({e2}).")

        db.commit()
        print("Schema Fix Complete.")

if __name__ == "__main__":
    fix_schema_nuclear()
