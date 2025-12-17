from app import app
from db import get_db

def check_exists():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute("DESCRIBE applications")
            print("Table 'applications' EXISTS.")
            for x in cursor.fetchall():
                print(x)
        except Exception as e:
            print(f"Table Check Failed: {e}")

if __name__ == "__main__":
    check_exists()
