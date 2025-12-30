# 🚀 IssueOut — IT Task Management System

# TasksManager

https://prnt.sc/SWdNGmeuZCla

**IssueOut** is a sophisticated task management platform tailored for software development teams. It leverages the power
of **Django** for a robust backend and **HTMX** for a dynamic, seamless user experience without redundant page reloads.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.x-092E20?style=for-the-badge&logo=django&logoColor=white)
![HTMX](https://img.shields.io/badge/HTMX-2.x-3D72D7?style=for-the-badge&logo=htmx&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)

---

## ✨ Key Features

* **🔒 Secure Authentication:** Custom registration flow with mandatory email activation via secure tokens.
* **📊 Smart Workspace:** Personalized dashboard with real-time statistics (total tasks, high priority, completion rate).
* **⚡ Reactive UI (HTMX Integration):**
    * Instant search and filtering of tasks.
    * Inline status toggling and dynamic content updates.
    * Infinite scroll/pagination for smooth task browsing.
    * Seamless modal integration for destructive actions (deletions).
* **🛠 Advanced Form Logic:** Custom JavaScript (`smart_button.js`) tracks field changes and only displays "Save/Cancel"
  buttons when the form is "dirty," preventing unnecessary requests.
* **📋 Agile Task Management:** Comprehensive CRUD for tasks, categorized by types (Bugs, Features, etc.) and priority
  levels.
* **🧪 Reliable Codebase:** Extensive test suite covering Models, Forms, Views, and Admin logic.

---

## 🛠 Tech Stack

* **Backend:** Python 3.x, Django.
* **Database:** SQLite (PostgreSQL compatible).
* **Frontend:** HTMX, Vanilla JavaScript, Bootstrap 5, Bootstrap Icons.
* **Forms:** Django Crispy Forms (Bootstrap 5 Pack).
* **Development Tools:** Django Debug Toolbar, `python-dotenv`.

---

## 🏗 Project Architecture

The system is modularized into two core applications:

1. **`landing`**: Handles public pages, user onboarding, email services, and token-based activation.
2. **`task`**: Contains the core business logic, including `Worker` (custom user model), `Task`, `TaskType`, and
   `Position`.

---

## 🚀 Local Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/issue-out.git](https://github.com/your-username/issue-out.git)
   cd issue-out
   ```

2. **Initialize Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configuration:**
   Create a `.env` file in the root directory and provide your settings (SECRET_KEY, Email host, etc.).

5. **Run Migrations & Server:**
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

---

## 🧪 Testing

Ensure system stability by running the tests:

```bash
python manage.py test

```

---


## Additional


**Current DB structure**
![Model](https://private-user-images.githubusercontent.com/45209469/529426044-de471b16-0fa6-40ab-8c33-416857f80eb7.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NjY0NDUzMTQsIm5iZiI6MTc2NjQ0NTAxNCwicGF0aCI6Ii80NTIwOTQ2OS81Mjk0MjYwNDQtZGU0NzFiMTYtMGZhNi00MGFiLThjMzMtNDE2ODU3ZjgwZWI3LnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNTEyMjIlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjUxMjIyVDIzMTAxNFomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTRhMWI3YmQ0YTY3OTI4NzJhMmQzNGU5ODdlMDhhZDQ0ODUyOWY4N2E2ZGNmMmVhNzdmZWU5ODU3MTY5NGY1ZDMmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.Da38e_YauinC6c1cT8ADGb-xppp_PGjy_rJf_7K-RqU)
