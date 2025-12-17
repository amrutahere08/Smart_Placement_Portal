from app import app
from db import get_db
import datetime

def seed_interviews():
    with app.app_context():
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        print("Seeding Interview Dates...")
        
        # 1. Get some applications
        cursor.execute("SELECT id FROM applications LIMIT 5")
        apps = cursor.fetchall()
        
        if not apps:
            print("No applications found to schedule.")
            return

        # 2. Schedule them
        # Set date to tomorrow 10:00 AM
        tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
        interview_date = tomorrow.replace(hour=10, minute=0, second=0, microsecond=0)
        
        for row in apps:
            app_id = row['id']
            # Update status and date
            sql = "UPDATE applications SET status = 'Interview Scheduled', interview_date = %s WHERE id = %s"
            cursor.execute(sql, (interview_date, app_id))
            print(f" -> Scheduled Interview for App ID {app_id} on {interview_date}")
            
        db.commit()
        print("Seeding Complete!")

if __name__ == "__main__":
    seed_interviews()
