import mysql.connector
from db import get_db
from app import app

def update_schema():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        
        print("Updating Database Schema for Phase 2...")

        # 1. Create 'applications' table
        print("Creating 'applications' table...")
        try:
            sql_app = """
            CREATE TABLE IF NOT EXISTS applications (
                id INT AUTO_INCREMENT PRIMARY KEY,
                student_id INT NOT NULL,
                company_id INT NOT NULL,
                status VARCHAR(50) DEFAULT 'Applied',
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            cursor.execute(sql_app)
            print(" -> 'applications' table created/verified.")
        except Exception as e:
            print(f" !!! Error creating table: {e}")

        # 2. Add 'resume' and 'cgpa' to 'studentlogin'
        print("Updating 'studentlogin' table...")

        def add_column_if_not_exists(table, col, def_type):
            try:
                cursor.execute(f"ALTER TABLE {table} ADD COLUMN {col} {def_type}")
                print(f" -> Added '{col}' column.")
            except mysql.connector.Error as err:
                 print(f" -> Info: Could not add '{col}' (might exist). Msg: {err}")
            except Exception as e:
                print(f" !!! Error adding column {col}: {e}")

        add_column_if_not_exists('studentlogin', 'resume', 'VARCHAR(255) DEFAULT NULL')
        add_column_if_not_exists('studentlogin', 'cgpa', 'FLOAT DEFAULT 0.0')
        add_column_if_not_exists('studentlogin', 'skills', 'TEXT DEFAULT NULL')
        
        # 3. Create 'resources' table
        print("Creating 'resources' table...")
        try:
            sql_res = """
            CREATE TABLE IF NOT EXISTS resources (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                link VARCHAR(255) NOT NULL,
                date_added DATE DEFAULT NULL
            )
            """
            cursor.execute(sql_res)
            print(" -> 'resources' table created/verified.")
        except Exception as e:
            print(f" !!! Error creating resources table: {e}")

        # 4. Add 'interview_date' to 'applications'
        print("Updating 'applications' table...")
        add_column_if_not_exists('applications', 'interview_date', 'DATETIME DEFAULT NULL')
        
        db.commit()
        print("Schema Update Complete!")

if __name__ == "__main__":
    update_schema()
