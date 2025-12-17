from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_mail import Mail, Message
from db import get_db, close_db
import os
from datetime import datetime
import csv
import io
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'static/resumes'

# --- EMAIL CONFIG (Feature 2) ---
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@gmail.com' # CHANGE THIS
app.config['MAIL_PASSWORD'] = 'your_app_password'    # CHANGE THIS
mail = Mail(app)

def send_notification(to, subject, body):
    try:
        msg = Message(subject, sender=app.config['MAIL_USERNAME'], recipients=[to])
        msg.body = body
        mail.send(msg)
        print(f"Email sent to {to}")
    except Exception as e:
        print(f"Email Failed (Check Attributes): {e}")
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Register database teardown
app.teardown_appcontext(close_db)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['uname']
        pwd = request.form['pwd1']
        
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        # Check Admin
        cursor.execute("SELECT * FROM adminlogin WHERE uname = %s AND pwd = %s", (uname, pwd))
        admin = cursor.fetchone()
        
        if admin:
            session['user_type'] = 'admin'
            session['username'] = admin['uname']
            session['user_id'] = admin['id']
            return redirect(url_for('admin_home'))
            
        # Check Student
        cursor.execute("SELECT * FROM studentlogin WHERE email = %s AND password = %s", (uname, pwd))
        student = cursor.fetchone()
        
        if student:
            session['user_type'] = 'student'
            session['username'] = student['fname'] # PHP used fname for session
            session['user_id'] = student['id']
            return redirect(url_for('student_home'))
            
        flash('Username and Password Wrong', 'danger')
        
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # uname, fname, lname, email, phone, pwd1, pwd2, secque, secans
        uname = request.form['username']
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['mailid']
        phone = request.form['phone']
        pwd1 = request.form['pwd1']
        pwd2 = request.form['pwd2']
        secque = request.form['secque']
        secans = request.form['secans']

        if pwd1 != pwd2:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('register'))

        db = get_db()
        cursor = db.cursor()
        
        # Check if user exists
        cursor.execute("SELECT * FROM studentlogin WHERE uname = %s OR email = %s", (uname, email))
        if cursor.fetchone():
            flash('Username or Email already exists.', 'danger')
            return redirect(url_for('register'))

        try:
            sql = "INSERT INTO studentlogin(uname, pwd, fname, lname, email, phone, secque, secans) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (uname, pwd1, fname, lname, email, phone, secque, secans))
            db.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except mysql.connector.Error as err:
            flash(f"Error: {err}", 'danger')
            return redirect(url_for('register'))

    return render_template('register.html')

@app.route('/post_feed', methods=['POST'])
def post_feed():
    if 'user_type' not in session or session['user_type'] != 'admin':
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        message = request.form['message']
        user = session['username']
        # Use current date/time
        import datetime
        now = datetime.datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H:%M:%S")
        
        db = get_db()
        cursor = db.cursor()
        sql = "INSERT INTO feed(user, message, date, time) VALUES(%s, %s, %s, %s)"
        cursor.execute(sql, (user, message, date_str, time_str))
        db.commit()
        return redirect(url_for('admin_home'))

@app.route('/admin')
def admin_home():
    if 'user_type' not in session or session['user_type'] != 'admin':
        return redirect(url_for('login'))
    
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    # Fetch Feed
    cursor.execute("SELECT * FROM feed ORDER BY date DESC, time DESC")
    feeds = cursor.fetchall()

    # Fetch Companies
    cursor.execute("SELECT * FROM company ORDER BY id DESC")
    companies = cursor.fetchall()

    # Analytics
    cursor.execute("SELECT count(*) as count FROM studentlogin")
    total_students = cursor.fetchone()['count']

    cursor.execute("SELECT count(*) as count FROM applications WHERE status = 'Selected'")
    placed_students = cursor.fetchone()['count']
    
    cursor.execute("SELECT count(*) as count FROM company")
    total_companies = cursor.fetchone()['count']
    
    # --- CHART DATA 1: Branch-wise Placed ---
    cursor.execute("""
        SELECT s.dept, COUNT(*) as count 
        FROM studentlogin s 
        JOIN applications a ON s.id = a.student_id 
        WHERE a.status='Selected' 
        GROUP BY s.dept
    """)
    branch_data = cursor.fetchall()
    branch_labels = [row['dept'] for row in branch_data]
    branch_counts = [row['count'] for row in branch_data]
    
    # --- CHART DATA 2: Applications per Company ---
    cursor.execute("""
        SELECT c.name, COUNT(*) as count 
        FROM applications a 
        JOIN company c ON a.company_id = c.id 
        GROUP BY c.name 
        ORDER BY count DESC LIMIT 5
    """)
    comp_data = cursor.fetchall()
    comp_labels = [row['name'] for row in comp_data]
    comp_counts = [row['count'] for row in comp_data]
    
    stats = {
        'students': total_students,
        'placed': placed_students,
        'unplaced': total_students - placed_students,
        'companies': total_companies,
        'branch_labels': branch_labels,
        'branch_counts': branch_counts,
        'comp_labels': comp_labels,
        'comp_counts': comp_counts
    }
    
    return render_template('admin/index.html', feed_items=feeds, companies=companies, stats=stats)

@app.route('/student')
def student_home():
    if 'user_type' not in session or session['user_type'] != 'student':
        return redirect(url_for('login'))
        
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    # Fetch Feed
    cursor.execute("SELECT * FROM feed ORDER BY date DESC, time DESC")
    feeds = cursor.fetchall()

    # Fetch Companies
    cursor.execute("SELECT * FROM company ORDER BY id DESC")
    companies = cursor.fetchall()
    
    return render_template('student/index.html', feed_items=feeds, companies=companies)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_type' not in session or session['user_type'] != 'student':
        return redirect(url_for('login'))
    
    db = get_db()
    cursor = db.cursor(dictionary=True)
    user_id = session['user_id']
    
    if request.method == 'POST':
        cgpa = request.form.get('cgpa')
        skills = request.form.get('skills')
        
        # Resume Upload
        if 'resume' in request.files:
            file = request.files['resume']
            if file and file.filename != '':
                filename = secure_filename(f"resume_{user_id}.pdf")
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                cursor.execute("UPDATE studentlogin SET resume = %s WHERE id = %s", (filename, user_id))
        
        cursor.execute("UPDATE studentlogin SET cgpa = %s, skills = %s WHERE id = %s", (cgpa, skills, user_id))
        db.commit()
        flash('Profile Updated!', 'success')
        return redirect(url_for('profile'))

    cursor.execute("SELECT * FROM studentlogin WHERE id = %s", (user_id,))
    student = cursor.fetchone()
    return render_template('student/profile.html', student=student)

@app.route('/apply/<int:company_id>')
def apply(company_id):
    if 'user_type' not in session or session['user_type'] != 'student':
        return redirect(url_for('login'))

    try:
        user_id = session['user_id']
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        # Check if already applied
        cursor.execute("SELECT * FROM applications WHERE student_id = %s AND company_id = %s", (user_id, company_id))
        if cursor.fetchone():
            flash('You have already applied!', 'warning')
            return redirect(url_for('student_home'))

        # Check Eligibility (Strict: Student CGPA >= Company B.Tech Check)
        cursor.execute("SELECT cgpa FROM studentlogin WHERE id = %s", (user_id,))
        student = cursor.fetchone()
        cursor.execute("SELECT btech FROM company WHERE id = %s", (company_id,))
        comp = cursor.fetchone()
        
        if student['cgpa'] and comp['btech']:
            student_score = float(student['cgpa'])
            if student_score <= 10:
                student_score = student_score * 10
            required_score = float(comp['btech'])
            
            if student_score < required_score:
                flash(f'Not Eligible! Required: {required_score}%, Your Score: {student_score}%', 'danger')
                return redirect(url_for('student_home'))
        
        # Fetch student resume to snapshot it for the application
        cursor.execute("SELECT resume_path FROM studentlogin WHERE id = %s", (user_id,))
        res_row = cursor.fetchone()
        resume_val = res_row['resume_path'] if res_row and res_row['resume_path'] else 'dummy.pdf'
        
        cursor.execute("INSERT INTO applications (student_id, company_id, resume) VALUES (%s, %s, %s)", (user_id, company_id, resume_val))
        db.commit()
        
        # Send Email Notification (Feature 2)
        try:
            cursor.execute("SELECT email, fname FROM studentlogin WHERE id=%s", (user_id,))
            stu = cursor.fetchone()
            cursor.execute("SELECT name FROM company WHERE id=%s", (company_id,))
            cmp = cursor.fetchone()
            
            if stu and cmp:
                send_notification(stu['email'], f"Applied to {cmp['name']}", f"Dear {stu['fname']},\n\nYou have successfully applied for the drive at {cmp['name']}.\n\nBest,\nPMS Team")
        except Exception as e:
            print(f"EMAIL ERROR (Ignored): {e}")

        flash('Applied Successfully!', 'success')
        return redirect(url_for('student_home'))

    except Exception as e:
        return f"CRITICAL ERROR IN APPLY: {str(e)}"

@app.route('/my_applications')
def my_applications():
    if 'user_type' not in session or session['user_type'] != 'student':
        return redirect(url_for('login'))
        
    db = get_db()
    cursor = db.cursor(dictionary=True)
    user_id = session['user_id']
    
    sql = """
    SELECT a.status, a.interview_date, c.name as company_name, c.curdate 
    FROM applications a 
    JOIN company c ON a.company_id = c.id 
    WHERE a.student_id = %s
    """
    cursor.execute(sql, (user_id,))
    apps = cursor.fetchall()
    return render_template('student/my_applications.html', applications=apps)

@app.route('/manage_company', methods=['GET', 'POST'])
def manage_company():
    if 'user_type' not in session or session['user_type'] != 'admin':
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['name']
        curdate = request.form['curdate'] # YYYY-MM-DD
        branch = request.form['branch']
        det = request.form['det']
        # Default criteria
        db = get_db()
        cursor = db.cursor()
        sql = "INSERT INTO company (name, curdate, branch, det, tenth, twelth, btech) VALUES (%s, %s, %s, %s, 60, 60, 60)"
        cursor.execute(sql, (name, curdate, branch, det))
        db.commit()
        flash('Company Added!', 'success')
        return redirect(url_for('admin_home'))
        
    return render_template('admin/add_company.html')

@app.route('/applicants/<int:company_id>')
def view_applicants(company_id):
    if 'user_type' not in session or session['user_type'] != 'admin':
        return redirect(url_for('login'))
        
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    sql = """
    SELECT s.fname, s.lname, s.email, s.contact, s.resume_path as resume, a.status, a.id as app_id
    FROM applications a
    JOIN studentlogin s ON a.student_id = s.id
    WHERE a.company_id = %s
    """
    cursor.execute(sql, (company_id,))
    applicants = cursor.fetchall()
    
    cursor.execute("SELECT id, name FROM company WHERE id = %s", (company_id,))
    company = cursor.fetchone()
    
    return render_template('admin/applicants.html', applicants=applicants, company=company)

@app.route('/update_status/<int:app_id>/<string:new_status>')
def update_status(app_id, new_status):
    if 'user_type' not in session or session['user_type'] != 'admin':
        return redirect(url_for('login'))
        
    db = get_db()
    cursor = db.cursor()
    cursor.execute("UPDATE applications SET status = %s WHERE id = %s", (new_status, app_id))
    db.commit()
    flash(f'Application Status Updated to {new_status}!', 'success')
    # We need to redirect back to the applicants list. 
    # Since we don't have company_id handy in this route, we can fetch it or just redirect to admin home.
    # A better way is to pass company_id or fetch it. Let's fetch it for redirect.
    cursor.execute("SELECT company_id FROM applications WHERE id = %s", (app_id,))
    res = cursor.fetchone()
    if res:
        return redirect(url_for('view_applicants', company_id=res[0]))
    return redirect(url_for('admin_home'))

@app.route('/admin/students')
def admin_students():
    if 'user_type' not in session or session['user_type'] != 'admin':
        return redirect(url_for('login'))
        
    filter_type = request.args.get('filter', 'all')
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    if filter_type == 'placed':
        sql = """
        SELECT DISTINCT s.*, c.name as company_name 
        FROM studentlogin s
        JOIN applications a ON s.id = a.student_id
        JOIN company c ON a.company_id = c.id
        WHERE a.status = 'Selected'
        """
        cursor.execute(sql)
    else:
        cursor.execute("SELECT * FROM studentlogin")
        
    students = cursor.fetchall()
    return render_template('admin/student_list.html', students=students, filter_type=filter_type)

@app.route('/admin/drives')
def admin_drives():
    if 'user_type' not in session or session['user_type'] != 'admin':
        return redirect(url_for('login'))
        
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM company ORDER BY curdate DESC")
    companies = cursor.fetchall()
    return render_template('admin/drives_list.html', companies=companies)

@app.route('/delete_company/<int:id>')
def delete_company(id):
    if 'user_type' not in session or session['user_type'] != 'admin':
        return redirect(url_for('login'))
        
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM company WHERE id = %s", (id,))
    db.commit()
    flash('Company Deleted Successfully!', 'warning')
    # Check referrer to redirect back to correct list
    if request.referrer and 'drives' in request.referrer:
        return redirect(url_for('admin_drives'))
    return redirect(url_for('admin_home'))

@app.route('/export_applicants/<int:company_id>')
def export_applicants(company_id):
    if 'user_type' not in session or session['user_type'] != 'admin':
        return redirect(url_for('login'))
    
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    # Fetch Data
    sql = """
    SELECT s.fname, s.lname, s.email, s.cgpa, s.phone, a.status 
    FROM applications a
    JOIN studentlogin s ON a.student_id = s.id
    WHERE a.company_id = %s
    """
    cursor.execute(sql, (company_id,))
    applicants = cursor.fetchall()
    
    # Generate CSV
    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(['First Name', 'Last Name', 'Email', 'CGPA', 'Phone', 'Status']) # Header
    
    for row in applicants:
        cw.writerow([row['fname'], row['lname'], row['email'], row['cgpa'], row['phone'], row['status']])
        
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = f"attachment; filename=applicants_{company_id}.csv"
    output.headers["Content-type"] = "text/csv"
    return output

@app.route('/schedule_interview/<int:app_id>', methods=['POST'])
def schedule_interview(app_id):
    if 'user_type' not in session or session['user_type'] != 'admin':
        return redirect(url_for('login'))
        
    date_str = request.form['interview_date'] # Expecting YYYY-MM-DDTHH:MM
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute("UPDATE applications SET interview_date = %s, status = 'Interview Scheduled' WHERE id = %s", (date_str, app_id))
    db.commit()
    
    flash('Interview Scheduled!', 'success')
     # Get company id for redirect
    cursor.execute("SELECT company_id FROM applications WHERE id = %s", (app_id,))
    res = cursor.fetchone()
    return redirect(url_for('view_applicants', company_id=res[0]))

@app.route('/resources', methods=['GET', 'POST'])
def resources():
    if 'user_type' not in session:
        return redirect(url_for('login'))
        
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    if request.method == 'POST':
        # Admin Only
        if session['user_type'] != 'admin':
             return redirect(url_for('login'))
             
        title = request.form['title']
        link = request.form['link']
        import datetime
        date_str = datetime.date.today()
        
        cursor.execute("INSERT INTO resources (title, link, date_added) VALUES (%s, %s, %s)", (title, link, date_str))
        db.commit()
        flash('Resource Added!', 'success')
        return redirect(url_for('resources'))
    
    cursor.execute("SELECT * FROM resources ORDER BY id DESC")
    res_list = cursor.fetchall()
    return render_template('student/resources.html', resources=res_list)

@app.route('/change_password', methods=['POST'])
def change_password():
    if 'user_type' not in session:
        return redirect(url_for('login'))
        
    user_id = session['user_id']
    table = 'studentlogin' if session['user_type'] == 'student' else 'adminlogin'
    
    new_pass = request.form['new_password']
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute(f"UPDATE {table} SET pwd = %s WHERE id = %s", (new_pass, user_id))
    db.commit()
    flash('Password Changed Successfully!', 'success')
    return redirect(url_for('profile') if session['user_type'] == 'student' else 'admin_home')

# Prevent Caching to fix navigation glitch
@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

# --- DEBUG ROUTE FOR DB FIX ---
@app.route('/debug_fix')
@app.route('/debug_fix')
def debug_fix():
    try:
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        
        # 1. Try Drop (Might fail 1824)
        try: cursor.execute("DROP TABLE IF EXISTS applications")
        except: pass
        try: cursor.execute("DROP TABLE IF EXISTS studentlogin")
        except: pass
        try: cursor.execute("DROP TABLE IF EXISTS company")
        except: pass
        
        # 2. Recreate/Restore Student
        # If Drop failed, this Create IF NOT EXISTS runs.
        sql_stu = """CREATE TABLE IF NOT EXISTS studentlogin (
            id INT AUTO_INCREMENT PRIMARY KEY,
            fname VARCHAR(100), lname VARCHAR(100), email VARCHAR(100) UNIQUE,
            password VARCHAR(100), contact VARCHAR(20), dept VARCHAR(50),
            batch VARCHAR(10), gender VARCHAR(10), resume_path VARCHAR(255) DEFAULT NULL,
            cgpa FLOAT DEFAULT 0.0, skills TEXT
        )"""
        cursor.execute(sql_stu)
        # Ensure student exists
        cursor.execute("INSERT IGNORE INTO studentlogin (fname, email, password) VALUES ('Student User', 'student@gmail.com', '123')")
        
        # 3. Recreate/Restore Company
        sql_com = """CREATE TABLE IF NOT EXISTS company (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100), det VARCHAR(255), curdate VARCHAR(50),
            branch VARCHAR(100), tenth FLOAT DEFAULT 60, twelth FLOAT DEFAULT 60,
            btech FLOAT DEFAULT 60, backlog INT DEFAULT 0
        )"""
        cursor.execute(sql_com)
        
        # 4. Recreate/Restore Applications
        sql_app = """CREATE TABLE IF NOT EXISTS applications (
            id INT AUTO_INCREMENT PRIMARY KEY,
            student_id INT, company_id INT, status VARCHAR(50) DEFAULT 'Applied',
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            interview_date DATETIME DEFAULT NULL, resume VARCHAR(255) DEFAULT NULL
        )"""
        cursor.execute(sql_app)
        
        # 5. Fix Schema & Clear Data (In case Drop failed)
        try: cursor.execute("ALTER TABLE applications MODIFY resume VARCHAR(255) DEFAULT NULL")
        except: pass
        cursor.execute("DELETE FROM applications") # Clear old
        
        # 6. Seed Companies
        companies = [
            ("Infosys", "System Engineer", "2025-12-12"),
            ("TCS", "Digital Profile", "2025-12-15"),
            ("Amazon", "SDE", "2024-03-10"),
            ("Oracle", "Dev", "2024-04-15"),
            ("Innovate Corp", "Dev", "2025-02-01"),
            ("Global Systems", "Analyst", "2025-02-10")
        ]
        cid_map = {}
        for name, role, date in companies:
            cursor.execute("DELETE FROM company WHERE name LIKE %s", (name + '%',)) # Avoid dupes
            cursor.execute("INSERT INTO company (name, det, curdate) VALUES (%s, %s, %s)", (name, role, date))
            cid_map[name] = cursor.lastrowid
            
        # 7. Seed Applications (With RESUME)
        cursor.execute("SELECT id FROM studentlogin")
        students = cursor.fetchall()
        for s in students:
            uid = s[0]
            def add_app(cname, status, idate):
                if cname in cid_map:
                    # Provide dummy resume to satisfy ANY constraint
                    cursor.execute("INSERT INTO applications (student_id, company_id, status, interview_date, resume) VALUES (%s, %s, %s, %s, 'dummy.pdf')", (uid, cid_map[cname], status, idate))
            
            add_app("Infosys", "Selected", "2025-12-12 10:00:00")
            add_app("TCS", "Rejected", "2025-12-15 10:00:00")
            add_app("Amazon", "Selected", "2024-03-10")
            add_app("Oracle", "Rejected", "2024-04-15")
            add_app("Innovate Corp", "Interview Scheduled", "2025-12-19")
            add_app("Global Systems", "Interview Scheduled", "2025-12-20")
        
        db.commit()
        return "DATABASE FIXED! REFRESH."
    except Exception as e:
        return f"ERROR: {str(e)}"


# --- FEATURE 3: INTERVIEW FORUM ---
@app.route('/experiences')
def experiences():
    if 'user_type' not in session: return redirect(url_for('login'))
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT e.*, s.fname, s.lname 
        FROM experiences e 
        JOIN studentlogin s ON e.student_id = s.id 
        ORDER BY created_at DESC
    """)
    posts = cursor.fetchall()
    return render_template('student/experiences.html', posts=posts)

@app.route('/share_experience', methods=['POST'])
def share_experience():
    if 'user_type' != 'student': return redirect(url_for('login'))
    company = request.form['company']
    role = request.form['role']
    questions = request.form['questions']
    tips = request.form['tips']
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO experiences (student_id, company_name, role, questions, tips)
        VALUES (%s, %s, %s, %s, %s)
    """, (session['user_id'], company, role, questions, tips))
    db.commit()
    flash('Experience Shared!', 'success')
    return redirect(url_for('experiences'))

# --- FEATURE 4: MOCK TEST ---
QUESTIONS = [
    {'id': 1, 'q': 'What is the complexity of Binary Search?', 'options': ['O(n)', 'O(log n)', 'O(n^2)', 'O(1)'], 'ans': 'O(log n)'},
    {'id': 2, 'q': 'Which data structure uses LIFO?', 'options': ['Queue', 'Stack', 'Tree', 'Graph'], 'ans': 'Stack'},
    {'id': 3, 'q': 'Full form of SQL?', 'options': ['Simple Query Language', 'Structured Query Language', 'System Query Logic', 'None'], 'ans': 'Structured Query Language'},
    {'id': 4, 'q': 'Python is interpreted?', 'options': ['True', 'False'], 'ans': 'True'},
    {'id': 5, 'q': 'HTTP Status 404 means?', 'options': ['Server Error', 'Not Found', 'OK', 'Unauthorized'], 'ans': 'Not Found'}
]

@app.route('/mock_test')
def mock_test():
    if 'user_type' not in session: return redirect(url_for('login'))
    return render_template('student/mock_test.html', questions=QUESTIONS)

@app.route('/submit_test', methods=['POST'])
def submit_test():
    score = 0
    total = len(QUESTIONS)
    for q in QUESTIONS:
        user_ans = request.form.get(f'q{q["id"]}')
        if user_ans == q['ans']:
            score += 1
    
    # Optional: Send Email on completion
    if session.get('user_type') == 'student':
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT email FROM studentlogin WHERE id=%s", (session['user_id'],))
        u = cursor.fetchone()
        if u:
            send_notification(u['email'], 'Mock Test Result', f'You scored {score}/{total}. Keep practicing!')
            
    return render_template('student/mock_result.html', score=score, total=total)

if __name__ == '__main__':
    app.run(debug=True)
