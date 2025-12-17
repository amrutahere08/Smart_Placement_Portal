from app import app
from db import get_db

def backfill_dates():
    with app.app_context():
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        print("Backfilling Dates for History...")
        
        # Update applications to have interview_date = curdate of company IF status is Selected/Rejected
        # This gives the user the 'Date' they requested.
        
        sql = """
        UPDATE applications a
        JOIN company c ON a.company_id = c.id
        SET a.interview_date = c.curdate
        WHERE a.status IN ('Selected', 'Rejected') AND a.interview_date IS NULL
        """
        
        cursor.execute(sql)
        db.commit()
        print(f"Updated {cursor.rowcount} records with dates.")

if __name__ == "__main__":
    backfill_dates()
