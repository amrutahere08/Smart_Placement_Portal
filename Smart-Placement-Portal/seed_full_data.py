from app import app
from db import get_db

def seed_full_data():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        
        print("Seeding Sample Resources...")
        resources = [
            ("Technical Interview Guide", "https://google.com", "2023-10-01"),
            ("Aptitude Test Papers", "https://example.com/aptitude", "2023-10-05"),
            ("HR Interview Questions", "https://example.com/hr", "2023-10-10"),
            ("Resume Building Tips", "https://example.com/resume", "2023-10-12")
        ]
        
        for title, link, date in resources:
            # Check exist
            cursor.execute("SELECT id FROM resources WHERE title = %s", (title,))
            if not cursor.fetchone():
                cursor.execute("INSERT INTO resources (title, link, date_added) VALUES (%s, %s, %s)", (title, link, date))
                print(f" -> Added Resource: {title}")
        
        print("Filling Missing Student Data...")
        # Update missing CGPA/Skills for demo
        cursor.execute("UPDATE studentlogin SET cgpa = 8.5 WHERE cgpa = 0 OR cgpa IS NULL")
        cursor.execute("UPDATE studentlogin SET skills = 'Python, SQL, Flask' WHERE skills IS NULL OR skills = ''")
        print(" -> Updated student profiles with dummy CGPA (8.5) and Skills.")
        
        db.commit()
        print("Seeding Complete!")

if __name__ == "__main__":
    seed_full_data()
