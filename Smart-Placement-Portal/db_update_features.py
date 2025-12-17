from app import app
from db import get_db
import mysql.connector

def update_schema():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        
        print("=== UPDATING SCHEMA FOR FEATURES 3 & 4 ===")
        
        # 1. Experiences Table
        print("1. Creating 'experiences' table...")
        sql_exp = """CREATE TABLE IF NOT EXISTS experiences (
            id INT AUTO_INCREMENT PRIMARY KEY,
            student_id INT,
            company_name VARCHAR(100),
            role VARCHAR(100),
            questions TEXT,
            tips TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )"""
        cursor.execute(sql_exp)
        
        # Seed one experience
        try:
            cursor.execute("SELECT count(*) FROM experiences")
            if cursor.fetchone()[0] == 0:
                cursor.execute("""
                    INSERT INTO experiences (student_id, company_name, role, questions, tips)
                    VALUES (1, 'Infosys', 'System Engineer', '1. Tell me about yourself.\n2. Explain your project.', 'Be confident and know your project inside out.')
                """)
                print("   - Seeded sample experience.")
        except:
            pass
            
        db.commit()
        print("=== SUCCESS: SCHEMA UPDATED ===")

if __name__ == "__main__":
    update_schema()
