# Smart Placement Portal 🎓

The **Smart Placement Portal** is a comprehensive web-based recruitment management system designed to streamline the placement process for educational institutions. It bridges the gap between students, administrators, and recruiters, offering a seamless platform for job postings, applications, and interview management.

---

## Features

### **For Students**
*   **Profile Management:** Create and update professional profiles with skills, CGPA, and resume uploads.
*   **Job Discovery:** Browsing generic job feeds and specific company drives.
*   **One-Click Application:** Apply for placement drives based on eligibility criteria (CGPA, Branch, etc.).
*   **Real-time Status:** Track application status (Applied, Interview Scheduled, Selected, Rejected).
*   **Mock Tests:** Built-in mock tests to prepare for technical interviews.
*   **Interview Experiences:** Read experiential feedback from seniors and peers.

### **For Administrators**
*   **Analytical Dashboard:** View real-time statistics on placements, company participation, and student performance (Branch-wise charts).
*   **Drive Management:** Add and manage company drives with specific eligibility constraints (10th, 12th, B.Tech %, Backlogs).
*   **Application Tracking:** View applicant lists, shortlist candidates, and update statuses.
*   **Interview Scheduling:** Schedule interviews and notify students.
*   **Export Data:** Download applicant lists as CSV files.
*   **Feed System:** Post updates and announcements to the student community.

---

## Tech Stack

*   **Language:** Python
*   **Web Framework:** Flask
*   **Database:** MySQL
*   **Frontend:** HTML5, CSS3, Bootstrap
*   **Libraries:** `flask-mail` (Notifications), `mysql-connector-python` (Database Driver)

---

## Prerequisites

Before you begin, ensure you have the following installed:
1.  **Python 3.x**: [Download Python](https://www.python.org/downloads/)
2.  **MySQL Server**: [Download MySQL](https://dev.mysql.com/downloads/installer/)

---

## Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/Smart-Placement-Portal.git
cd Smart-Placement-Portal
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Database Configuration
You have **two options** to set up the database:

**Option A: Manual Import (Recommended)**
1.  Open your MySQL Workbench or Command Line.
2.  Create a database named `placement`.
3.  Import the provided SQL file located at `sql/placement.sql`.

**Option B: Auto-Fix Route**
1.  Ensure your database credentials match the code (see Step 4).
2.  Run the application first (Step 5).
3.  Visit `http://127.0.0.1:5000/debug_fix` in your browser. This will attempt to create tables and seed dummy data automatically.

### 4. Configure Application
Open `db.py` and update the database credentials if yours are different:
```python
# db.py
g.db = mysql.connector.connect(
    host="localhost",
    user="root",             # Change to your MySQL username
    password="yourpassword", # Change to your MySQL password
    database="placement"
)
```

Open `app.py` and configure the email settings for notifications to work:
```python
# app.py (Lines 18-19)
app.config['MAIL_USERNAME'] = 'your_email@gmail.com' 
app.config['MAIL_PASSWORD'] = 'your_app_password' # Use App Password, not login password
```

### 5. Run the Application
```bash
python app.py
```
The application will start at: `http://127.0.0.1:5000/`

---

## Login Credentials (Default)

The `sql/placement.sql` file comes with pre-seeded users. You can use these to log in immediately.

### **Admin Login**
*   **Username:** `admin1`
*   **Password:** `123`

### **Student Login**
*   **Username:** `naveen` (or `email`: `naveenrs@gmail.com`)
*   **Password:** `12345`

_Note: You can register new students via the Register page._

---

## Usage Workflow

1.  **Admin Setup:** Log in as Admin. Go to "Manage Company" to post a new job drive.
2.  **Student Apply:** Log in as Student. View the "Companies" list or "Feed". valid drives will appear. Click "Apply".
    *   *Constraint Check:* The system will block applications if your CGPA is lower than the company's requirement.
3.  **Process Application:** Admin goes to "View Applicants", sees the new application, and changes status to "Interview Scheduled" or "Selected".
4.  **Notification:** Student checks "My Applications" to see the status update.

---

## Troubleshooting

*   **Database Connection Error:** Ensure MySQL server is running and credentials in `db.py` are correct.
*   **Email Failed:** Ensure you are using an **App Password** for Gmail (not your regular password) and that 2-Factor Authentication is enabled on your Google Account.
*   **Module Not Found:** Run `pip install -r requirements.txt` again.
