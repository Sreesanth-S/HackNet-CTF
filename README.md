# HackNet CTF - Django Web Application

A cybersecurity-themed Capture The Flag (CTF) challenge built with Django. This web application simulates a login system with hidden flags and security challenges for educational purposes.

## 🎯 Project Overview

HackNet CTF is a web-based security challenge that includes:
- User authentication system
- Hidden flag challenges
- Cookie-based security testing
- Session management
- Admin panel for monitoring attempts

## 🚀 Features

- **Secure Login System**: Custom authentication with hardcoded credentials for CTF purposes
- **Flag Submission**: Submit and validate CTF flags
- **Cookie Management**: Automatic cookie setting for browser-based challenges
- **Session Tracking**: Monitor user sessions and attempts
- **Admin Interface**: Django admin panel to view submissions and user activity
- **CSRF Protection**: Built-in Django CSRF protection
- **Responsive Design**: Mobile-friendly interface

## 🛠️ Technology Stack

- **Backend**: Django 4.2+
- **Database**: SQLite (development) / PostgreSQL (production ready)
- **Frontend**: HTML5, CSS3, JavaScript
- **Deployment**: Gunicorn + Whitenoise (static files)
- **Security**: Django's built-in security features

## 📋 Prerequisites

- Python 3.8+
- pip (Python package manager)
- Git

## 🔧 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/hacknet-ctf.git
cd hacknet-ctf
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
```

### 5. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 6. Run Development Server
```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000`

## 🔐 Security Features

- **CSRF Protection**: All forms protected with CSRF tokens
- **Session Management**: Secure session handling with expiry
- **Input Validation**: Server-side validation for all inputs
- **XSS Prevention**: Django's built-in XSS protection
- **Cookie Security**: HttpOnly and SameSite cookie attributes

## ⚠️ Disclaimer

This application is designed for educational purposes and cybersecurity training. The intentional security vulnerabilities are for learning purposes only. Do not use in production environments without proper security hardening.

---

**Happy Hacking!** 🚩

*Built with ❤️ for cybersecurity education*
