echo "# 🚂 IRCTC Booking System (Django + Frontend)

This is a simple IRCTC-like booking system built with **Django (backend)** and plain **HTML/CSS/JS (frontend)**.  
It supports:

- User Registration & Login (with Aadhaar + phone)
- JWT-based authentication
- Ticket booking & cancellation
- PNR status checking
- Booking history per user

---

## ⚙️ Setup Instructions

### 1. Clone the repository

\`\`\`bash
git clone https://github.com/Hariharanx30/IRCTC.git
cd IRCTC
\`\`\`

### 2. Create and activate virtual environment

Windows:
\`\`\`bash
python -m venv venv
venv\\Scripts\\activate
\`\`\`

Mac/Linux:
\`\`\`bash
python3 -m venv venv
source venv/bin/activate
\`\`\`

### 3. Install dependencies

\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 4. Run migrations

\`\`\`bash
python manage.py migrate
\`\`\`

### 5. Create a superuser

\`\`\`bash
python manage.py createsuperuser
\`\`\`

### 6. Run the server

\`\`\`bash
python manage.py runserver
\`\`\`

Server runs at: **http://127.0.0.1:8000/**

---

## 📂 Project Structure

\`\`\`
.
├── core/  
├── templates/  
├── static/  
├── manage.py
├── requirements.txt
└── README.md
\`\`\`

---

## 🚀 Features

- Register/Login with Aadhaar + phone
- Book, Cancel, View History
- Check PNR status
- JWT Authentication

---

## 🔑 Default URLs

Frontend:

- /login/
- /register/
- /home/
- /booking/
- /history/
- /pnr/
- /cancel/
- /tourism/

APIs:

- /api/login/
- /api/me/
- /api/bookings/
- /api/book/
- /api/cancel/
- /api/pnr/<pnr>/
  " > README.md
