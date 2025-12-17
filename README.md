# Smart Placement Portal 🎓

The **Smart Placement Portal** is a comprehensive web-based recruitment management system designed to streamline the placement process for educational institutions. It bridges the gap between students, administrators, and recruiters, offering a seamless platform for job postings, applications, and interview management.

## 🚀 Features

### 👨‍🎓 **For Students**
*   **Profile Management:** Create and update professional profiles with skills, CGPA, and resume uploads.
*   **Job Application:** Browse and apply for placement drives based on eligibility criteria.
*   **Real-time Status:** Track application status (Applied, Interview Scheduled, Selected, Rejected).
*   **Mock Tests:** Practice with built-in mock tests to prepare for technical interviews.
*   **Interview Experiences:** Read and share interview experiences with peers.

### 👨‍💻 **For Administrators**
*   **Dashboard:** View real-time analytics on placements, company participation, and student performance.
*   **Company Management:** Add and manage company drives with specific eligibility criteria.
*   **Application Tracking:** View applicants, shortlist candidates, and update application statuses.
*   **Email Notifications:** Automated emails to students for application updates.
*   **Export Data:** Export applicant lists to CSV for offline processing.

## 🛠️ Tech Stack

*   **Backend:** Python (Flask)
*   **Database:** MySQL
*   **Frontend:** HTML5, CSS3, Bootstrap
*   **Libraries:** `flask-mail`, `mysql-connector-python`

## ⚙️ Installation & Setup

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/yourusername/Smart-Placement-Portal.git
    cd Smart-Placement-Portal
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Database Configuration**
    *   Set up a MySQL database.
    *   Import the schema 
    *   Update database credentials in `db.py` or `app.py`.

4.  **Email Configuration**
    *   Update `dest_email` and `password` in `app.py` for email notifications to work.

5.  **Run the Application**
    ```bash
    python app.py
    ```
    The application will run at `http://127.0.0.1:5000/`.

## 📸 Usage

1.  **Register/Login:** Students and Admins can log in to their respective dashboards.
2.  **Admin:** Post a new drive from the "Manage Company" section.
3.  **Student:** Apply for the drive if eligible.
4.  **Admin:** Review applicants and schedule interviews.
