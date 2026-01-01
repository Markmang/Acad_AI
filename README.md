# ðŸ“š ACAD AI â€“ MINI ASSESSMENT ENGINE API

Acad_AI is a powerful Django REST API that allows teachers and institutions to create exams, manage students, and automatically grade both MCQ and Theory questions intelligently. Students can register, authenticate, take exams, submit responses, and receive meaningful performance feedback instantly.

This project demonstrates strong backend engineering, authentication security, structured API workflow, intelligent keyword-based grading logic, and professional backend system design suitable for production-level exam platforms.

---

## âœ¨ FEATURES
- ðŸ‘¨â€ðŸ« Staff/Admin create & manage exams
- ðŸ‘¨â€ðŸŽ“ Students register, login, and take exams
- ðŸ§  Supports **MCQ + Theory** questions
- ðŸ“¡ Fully usable via Browser or Postman
- ðŸ” Secure **JWT Authentication**
- â›” Prevents duplicate submissions
- â³ Timed exam support
- ðŸ§¾ Intelligent **keyword-based grading engine**
- ðŸ—‚ SQLite ready out-of-the-box
- ðŸŽ¯ Detailed scoring, percentage & performance feedback
- ðŸ’¥ Clean error handling

---

## ðŸ§  TECH STACK
Python  
Django  
Django REST Framework  
JWT Authentication  
SQLite Database  

---

## ðŸš€ PROJECT SETUP

### ðŸ”½ Clone Repository
```bash
git clone https://github.com/Markmang/Acad_AI.git
cd Acad_AI
```

### ðŸ› ï¸ Create Virtual Environment
```bash
python -m venv venv
```

### â–¶ï¸ Activate Virtual Environment
**Windows**
```bash
venv\Scripts\activate
```

**Mac/Linux**
```bash
source venv/bin/activate
```

### ðŸ“¦ Install Dependencies
```bash
pip install -r requirements.txt
```

### ðŸ—„ Run Migrations
```bash
python manage.py migrate
```

### â–¶ï¸ Start Server
```bash
python manage.py runserver
```

Server runs at:
```
http://localhost:8000
```

---

## ðŸ—„ DATABASE
SQLite is included.  
No external setup required.  

---

## ðŸ” AUTHENTICATION SYSTEM
The system uses **JWT Authentication**.  
Without logging in, protected routes cannot be accessed.

---

## ðŸ‘¥ USER TYPES

### ðŸ›¡ SUPERUSER / STAFF Can:
- Login to Django Admin  
- Create Exams  
- Create MCQ and Theory Questions  
- Manage Exam Data  

---

### ðŸ‘¨â€ðŸŽ“ STUDENTS Can:
- Register  
- Login  
- View assigned exams  
- Start exams  
- Submit exams  
- Receive grading feedback  

---

## ðŸ“¸ SCREENSHOTS
| Questions List | Start Exam | Submit Success |
|----------------|------------|----------------|
| ![Questions](screenshots/questions_list.jpg) | ![Start](screenshots/start_exam.jpg) | ![Submit](screenshots/submit_success.jpg) |

---

## ðŸŒ REGISTRATION & LOGIN â€” BROWSABLE API

### âœ… STEP 1 â€” Register Student
**Endpoint:**
```
POST /api/register/
```

**Request Body**
```json
{
  "username": "student1",
  "password": "password123",
  "email": "student@email.com"
}
```

---

### âœ… STEP 2 â€” Login
```
POST /api/auth/login/
```

Returns:
```
access
refresh
```

Copy ACCESS TOKEN

---

### âœ… STEP 3 â€” Authenticate Browser
Click:
```
Login / Authenticate
```
Select:
```
Bearer Token
```
Paste Token

---

## ðŸ§ª STUDENT EXAM FLOW (BROWSER)

### ðŸ“¥ View Exam Questions
```
GET /api/exams/<exam_id>/questions/
```

Example:
```
GET /api/exams/1/questions/
```

---

### â–¶ï¸ Start Exam (Required)
```
POST /api/exams/1/start/
```

---

### ðŸ“¤ Submit Exam
```
POST /api/exams/1/submit/
```

Body Example
```json
{
  "answers": [
    { "question": 1, "answer": "Chlorophyll" },
    { "question": 2, "answer": "ear" },
    { "question": 5, "answer": "A cell is the basic unit of life" }
  ]
}
```

---

## ðŸ“Œ POSTMAN / THUNDER CLIENT FLOW

### STEP 1 â€” Register
```
POST http://localhost:8000/api/register/
```

### STEP 2 â€” Login
```
POST http://localhost:8000/api/auth/login/
```

Copy access token

### STEP 3 â€” Set Token
Auth Tab â†’ Bearer Token  
Paste Token  

Or Header:
```
Authorization: Bearer <token>
```

### STEP 4 â€” Student Actions
```
GET http://localhost:8000/api/exams/1/questions/
POST http://localhost:8000/api/exams/1/start/
POST http://localhost:8000/api/exams/1/submit/
```

---

## ðŸ›¡ EXAM SECURITY RULES
- Student must start exam before submitting  
- Student cannot submit twice  
- Student cannot submit another userâ€™s exam  
- Exam countdown starts after starting  
- Expired exams block submission  
- Safe failure handling  

---

## ðŸ§‘â€ðŸ« STAFF & ADMIN

### Create Superuser
```bash
python manage.py createsuperuser
```

Login:
```
http://localhost:8000/admin/
```

Create Staff + Assign Privileges

---

## ðŸ“ STAFF CREATES EXAM
```
POST /api/exams/
```

Example
```json
{
  "title": "Biology Test",
  "course": "Biology 101",
  "duration": 60,
  "metadata": {
    "level": "Intermediate",
    "topic": "Cells and Anatomy"
  }
}
```

---

## âž• ADD MCQ QUESTION
```
POST /api/exams/<exam_id>/questions/add/
```

```json
{
  "text": "Where is the smallest bone?",
  "question_type": "MCQ",
  "marks": 2,
  "options": ["ear", "leg", "nose", "arm"],
  "correct_answer": "ear"
}
```

---

## ðŸ§  ADD THEORY QUESTION
```json
{
  "text": "What is a cell?",
  "question_type": "THEORY",
  "marks": 5,
  "expected_keywords": [
    "smallest",
    "basic unit of life",
    "processes"
  ]
}
```

---

## ðŸ§® GRADING ENGINE

### MCQ
âœ” Correct â†’ Full marks  
âŒ Wrong â†’ 0  

### THEORY
âœ” Intelligent keyword-based grading  
âœ” Partial scoring  
âœ” Feedback shows matched + expected keywords  

---

## ðŸ OVERALL SCORE
Percentage:
```
(total score / total marks) * 100
```

Feedback:
- 85â€“100 = Excellent
- 70â€“84 = Good
- 50â€“69 = Fair
- Below 50 = Poor

---

## ðŸ§© FRONTEND INTEGRATION
Works with:
React  
Next.js  
Vue  
Flutter  
Android  
iOS  

Student Journey:
Login â†’ Token â†’ Fetch â†’ Start â†’ Answer â†’ Submit â†’ Results

---

## ðŸ‘¤ AUTHOR
Udeagha Mark Mang  
Backend Engineer  
Python | Django | Problem Solver  
