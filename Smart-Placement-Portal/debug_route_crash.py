from app import app
from db import get_db
from flask import render_template
import traceback

def debug_route():
    with app.app_context():
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        print("Debugging Route Crash...")
        
        # 1. Simulate finding student
        cursor.execute("SELECT id FROM studentlogin LIMIT 1")
        s = cursor.fetchone()
        if not s:
            print("No students found.")
            return
        uid = s['id']
        print(f"Testing for Student ID: {uid}")

        try:
            # 2. Run the exact query from my_applications
            print("Running SQL Query...")
            sql = """
            SELECT a.status, a.interview_date, c.name as company_name, c.curdate 
            FROM applications a 
            JOIN company c ON a.company_id = c.id 
            WHERE a.student_id = %s
            """
            cursor.execute(sql, (uid,))
            apps = cursor.fetchall()
            print(f"Query OK. Fetched {len(apps)} rows.")
            
            # Print row types to check for serialization issues
            if apps:
                r = apps[0]
                print("Sample Row:", r)
                print("Types:", {k: type(v) for k, v in r.items()})

            # 3. Try to render the template (if possible without request context, might fail)
            # This is hard to test outside request but meaningful.
            # We can just check data.
            
        except Exception:
            print("CRASHED during DB Operation:")
            traceback.print_exc()

if __name__ == "__main__":
    debug_route()
