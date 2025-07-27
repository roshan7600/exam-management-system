# 🎓 Exam Management System

A full-featured, role-based online exam platform built using **Django**. 
It supports **Admin**, **Teacher**, and **Student** roles with features like exam creation, real-time exam taking, auto-grading, analytics, and secure authentication.

---

## 📋 Table of Contents

- [✨ Features](#-features)
- [🏗️ System Architecture](#-system-architecture)
- [🚀 Quick Start](#-quick-start)
- [📦 Installation](#-installation)
- [🔧 Configuration](#-configuration)
- [📱 Usage](#-usage)
- [🎯 User Roles](#-user-roles)
- [📊 Database Schema](#-database-schema)
- [🧪 Testing](#-testing)
- [📸 Screenshots](#-screenshots)

---

## ✨ Features

### 🎯 Core Functionality
- **Multi-Role Authentication** – Admin, Teacher, and Student roles with access control
- **Course Management** – Manage academic courses easily
- **Exam Creation** – Flexible exam builder with MCQs and written questions
- **Real-time Exam Taking** – Secure, timed exams
- **Automated Grading** – Instant result processing and analytics
- **Result Management** – View results with performance tracking

### 🔐 Security Features
- **Secure Authentication** – Hashed passwords, CSRF protection
- **Role-based Permissions** – Only authorized users can access specific views
- **Exam Security** – Timers, one-attempt rules, and anti-cheating measures
- **Validation** – Input and form validation to prevent misuse

### 📊 Analytics & Reporting
- **Dashboards** – Student & teacher analytics dashboards
- **Grade Reports** – Detailed results and performance tracking
- **Export Options** – Export grades as CSV or PDF
- **Statistical Charts** – View class-wise and exam-wise stats

### 🎨 User Experience
- **Responsive Design** – Mobile-friendly interface using Bootstrap 5
- **Modern UI** – Clean and intuitive design
- **Real-time Updates** – Live feedback and updates during exams
- **Accessibility** – WCAG-compliant UI/UX

---

## 🏗️ System Architecture

Presentation Layer:

HTML, CSS, JavaScript, Bootstrap 5

Application Layer:

Django Views, Templates, Forms

Business Logic Layer:

Django Models, Services, Utilities

Data Layer:

SQLite (or PostgreSQL), Django ORM, Migrations



---

🚀 Quick Start
Get the Exam Management System up and running in just a few minutes!

Prerequisites
Python 3.8+ installed
Git installed
Basic knowledge of Django (optional)
One-Command Setup
```bash

Clone and setup everything
git clone https://github.com/roshan7600/exam-management-system.git cd exam-management-system python scripts/complete_setup.py

Manual Setup
```bash

1. Clone the repository
git clone https://github.com/roshan7600/exam-management-system.git cd exam-management-system

2. Create virtual environment
python -m venv exam_env source exam_env/bin/activate # On Windows: exam_env\Scripts\activate

3. Install dependencies
pip install -r requirements.txt

4. Setup database
python manage.py migrate

5. Create superuser
python manage.py createsuperuser

6. Load sample data (optional)
python scripts/seed_sample_data.py

7. Run the server
python manage.py runserver ```

🎉 That's it! Visit http://127.0.0.1:8000 to see your exam system in action!

📦 Installation
System Requirements
Python: 3.8 or higher
Django: 4.2+
Database: SQLite (default) or PostgreSQL
Memory: 512MB RAM minimum
Storage: 100MB free space
Dependencies
```txt Django>=4.2.0 Pillow>=9.0.0 python-docx>=0.8.11 matplotlib>=3.5.0 reportlab>=3.6.0 ```

Environment Setup
Clone Repository ```bash git clone https://github.com/roshan7600/exam-management-system.git cd exam-management-system ```

Virtual Environment ```bash python -m venv venv source venv/bin/activate # Linux/Mac venv\Scripts\activate # Windows ```

Install Dependencies ```bash pip install -r requirements.txt ```

Database Migration ```bash python manage.py makemigrations python manage.py migrate ```

Create Admin User ```bash python manage.py createsuperuser ```

🔧 Configuration
Environment Variables
Create a .env file in the project root:

```env

Django Settings
SECRET_KEY=your-secret-key-here DEBUG=True ALLOWED_HOSTS=localhost,127.0.0.1

Database Configuration
DATABASE_URL=sqlite:///db.sqlite3
