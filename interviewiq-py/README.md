# InterviewIQ — Flask + MySQL + HTML/CSS/JS

AI-powered interview coach. Single Flask server serves both the API and the frontend HTML pages.

---

## STEP-BY-STEP SETUP & RUN GUIDE

---

### STEP 1 — Check Python version

Open a terminal and run:

```
python --version
```

You need **Python 3.9 or higher**. Download from https://python.org if needed.

---

### STEP 2 — Set up MySQL database

1. Open **MySQL Workbench** (or any MySQL client)
2. Connect to your local MySQL server
3. Open the file `sql/schema.sql` from this project
4. Run the entire file — this creates the `interviewiq` database and all tables

Or from terminal:
```
mysql -u root -p < sql/schema.sql
```

---

### STEP 3 — Configure your environment

The `.env` file is already included with your credentials. Open it to verify or update:

```
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=
DB_NAME=interviewiq

GMAIL_USER=maruthipojar154@gmail.com
GMAIL_APP_PASSWORD=

GROQ_API_KEY=
GROQ_MODEL=openai/gpt-oss-20b
```

> **Important:** If the Groq API key stops working, get a free new one at https://console.groq.com

---

### STEP 4 — Create a virtual environment

In your terminal, navigate to the project folder:

```
cd interviewiq-py
```

Create a virtual environment:

```
python -m venv venv
```

Activate it:

- **Windows (PowerShell):**
  ```
  venv\Scripts\Activate.ps1
  ```

- **Windows (Command Prompt):**
  ```
  venv\Scripts\activate.bat
  ```

- **Mac / Linux:**
  ```
  source venv/bin/activate
  ```

You should see `(venv)` appear at the start of your terminal line.

---

### STEP 5 — Install dependencies

```
pip install -r requirements.txt
```

This installs Flask, mysql-connector-python, PyJWT, bcrypt, and all other packages.

---

### STEP 6 — Run the server

```
python app.py
```

You should see:
```
✅ MySQL connected: interviewiq
🚀 InterviewIQ backend running on http://localhost:5000
```

---

### STEP 7 — Open in browser

Go to: **http://localhost:5000**

That's it! The app is fully running.

---

## PROJECT STRUCTURE

```
interviewiq-py/
├── app.py                  ← Flask app entry point (run this)
├── config.py               ← Loads settings from .env
├── extensions.py           ← MySQL connection pool
├── requirements.txt        ← Python dependencies
├── .env                    ← Your credentials (don't share/commit this)
├── sql/
│   └── schema.sql          ← Run once in MySQL to create tables
├── models/
│   ├── user.py             ← User DB queries
│   ├── otp.py              ← OTP create/verify
│   ├── profile.py          ← Profile DB queries
│   ├── project.py          ← Project DB queries
│   └── session.py          ← Analytics session queries
├── routes/
│   ├── auth_routes.py      ← /api/auth/* (register, login, OTP, reset)
│   ├── profile_routes.py   ← /api/profile/*
│   ├── project_routes.py   ← /api/projects/*
│   ├── chat_routes.py      ← /api/chat (calls Groq AI)
│   ├── analytics_routes.py ← /api/analytics/*
│   └── page_routes.py      ← Serves HTML pages
├── utils/
│   ├── jwt_utils.py        ← JWT sign/verify
│   ├── mailer.py           ← Gmail OTP emails
│   └── decorators.py       ← @require_auth decorator
├── templates/              ← HTML pages (Jinja2)
│   ├── _base.html          ← Shared <head>, scripts
│   ├── login.html
│   ├── register.html
│   ├── verify_otp.html
│   ├── forgot_password.html
│   ├── reset_password.html
│   ├── dashboard.html
│   ├── profile.html
│   ├── resume.html
│   ├── projects.html
│   ├── chatbot.html
│   └── analytics.html
├── static/
│   ├── css/main.css        ← All styling (dark theme, responsive)
│   └── js/
│       ├── api.js          ← Fetch wrapper with JWT
│       ├── auth.js         ← Login/logout state
│       ├── toast.js        ← Toast notifications
│       └── layout.js       ← Sidebar shell (rendered in each page)
└── uploads/                ← Uploaded files (auto-created)
    ├── photos/
    ├── resumes/
    └── projects/
```

---

## COMMON ERRORS & FIXES

| Error | Fix |
|-------|-----|
| `MySQL connection failed` | Check DB_PASSWORD in .env, make sure MySQL is running |
| `AI service rejected the API key` | Get a new free key at https://console.groq.com |
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` with venv activated |
| `Address already in use` | Another process is on port 5000. Change PORT in .env or kill the process |
| OTP email not arriving | Check Gmail App Password — it must be a 16-char app password, not your Gmail password |

---

## STOPPING THE SERVER

Press `Ctrl + C` in the terminal where the server is running.

## RESTARTING

```
python app.py
```

(Make sure venv is still activated — you'll see `(venv)` in the terminal.)
