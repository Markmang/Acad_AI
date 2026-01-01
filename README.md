# Acad_AI
ACAD AI – MINI ASSESSMENT ENGINE API

This project is a Django REST API for an exam system where Staff/Admin can create exams and questions, while Students can take exams, submit answers, and receive automated grading and feedback.

It supports:

MCQ Questions

Theory Questions with intelligent keyword-based partial grading

Timed exams

Student must START exam before submitting

Prevents multiple submissions

Secure authentication

Fully usable via Browser or Postman / Thunder Client

TECH STACK

Python
Django
Django REST Framework
JWT Authentication
SQLite Database

PROJECT SETUP

Clone Repository
git clone <your github repo link>
cd Acad_AI

Create Virtual Environment
python -m venv venv

Activate Virtual Environment
Windows:
venv\Scripts\activate
Mac/Linux:
source venv/bin/activate

Install Dependencies
pip install -r requirements.txt

Run Migrations
python manage.py migrate

Start Server
python manage.py runserver

Server runs at:
http://localhost:8000

DATABASE

SQLite is included. No setup required.

AUTHENTICATION SYSTEM

The system uses JWT Authentication.
Without logging in, you cannot perform protected student or staff actions.

USER TYPES

SUPERUSER / STAFF
Can:

Login to Django Admin

Create Exams

Create MCQ and Theory Questions

Manage Exam Data

STUDENTS
Can:

Register

Login

View exams assigned

Start exams

Submit exams

Get grading feedback

REGISTRATION AND LOGIN - BROWSABLE API FLOW

STEP 1: REGISTER A STUDENT ACCOUNT
Endpoint:
POST /api/register/

Request Body:
{
"username": "student1",
"password": "password123",
"email": "student@email.com
"
}

After registration, student can login.

STEP 2: LOGIN (BROWSABLE API)

Go to:
POST /api/auth/login/

Enter:
username
password

Server will return:
access token
refresh token

Copy the ACCESS TOKEN.

STEP 3: AUTHENTICATE BROWSABLE API

In top right corner of Django Browsable API:
Click "Login / Authenticate"
Choose "Bearer / JWT Token"
Paste access token.

Now the student is authenticated.

STEP 4: STUDENT TAKES EXAM (FULL FLOW IN BROWSER)

View exam questions
GET /api/exams/<exam_id>/questions/

Example:
GET /api/exams/1/questions/

Start exam (required before submit)
POST /api/exams/1/start/

If student tries submitting without starting, server will reject gracefully.

Submit Exam
POST /api/exams/1/submit/

Example Body:
{
"answers": [
{ "question": 1, "answer": "Chlorophyll" },
{ "question": 2, "answer": "ear" },
{ "question": 5, "answer": "A cell is the basic unit of life" }
]
}

Response Returned:

Each question grading

Each question feedback

Total marks

Total score

Percentage

Overall Exam Performance Comment

Example Final Feedback Types:
Excellent performance
Good job
Fair attempt
Poor performance

REGISTRATION AND LOGIN - POSTMAN / THUNDER CLIENT
STEP 1: REGISTER STUDENT

POST http://localhost:8000/api/register/

Body:
{
"username": "student1",
"password": "password123",
"email": "student@email.com
"
}

STEP 2: LOGIN TO GET TOKEN

POST http://localhost:8000/api/auth/login/

Body:
{
"username": "student1",
"password": "password123"
}

Response Contains:
access
refresh

Copy ACCESS

STEP 3: SET AUTH TOKEN IN POSTMAN

Open request
Go to "Auth" tab
Choose Bearer Token
Paste access token

OR manually add header
Authorization: Bearer <TOKEN>

STEP 4: STUDENT EXAM FLOW IN POSTMAN

Get Questions
GET http://localhost:8000/api/exams/1/questions/

Start exam
POST http://localhost:8000/api/exams/1/start/

Submit exam
POST http://localhost:8000/api/exams/1/submit/

Body Example:
{
"answers": [
{ "question": 1, "answer": "Chlorophyll" },
{ "question": 2, "answer": "ear" },
{ "question": 5, "answer": "A cell is the basic unit of life" }
]
}

EXAM SECURITY RULES

Student must start exam before submitting
Student cannot submit twice
Student cannot submit another student exam
Exam is timed from START time not creation time
If time over → submission blocked safely
Handles errors gracefully without crashing

STAFF AND ADMIN USAGE
CREATE SUPERUSER

python manage.py createsuperuser

Login to:
http://localhost:8000/admin/

CREATE STAFF

In admin panel:

Create user

Assign staff privileges

STAFF CREATES EXAM

POST /api/exams/

Body:
{
"title": "Biology Test",
"course": "Biology 101",
"duration": 60,
"metadata": {
"level": "Intermediate",
"topic": "Cells and Anatomy"
}
}

STAFF ADDS MCQ QUESTION

POST /api/exams/<exam_id>/questions/add/

Body Example:
{
"text": "Where is the smallest bone?",
"question_type": "MCQ",
"marks": 2,
"options": ["ear", "leg", "nose", "arm"],
"correct_answer": "ear"
}

STAFF ADDS THEORY QUESTION

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

STAFF CAN ALSO:

Use Admin Panel to manage questions and exams
Edit questions
Delete questions
Modify duration
View submissions

GRADING ENGINE

MCQ
Correct answer → full marks
Wrong answer → zero
Feedback included

THEORY
Keyword based intelligent grading:
Detects how many expected points student hits
Partial scores supported
Feedback includes:
Matched keywords
Expected full keywords list

OVERALL EXAM SCORE

Percentage calculated:
(total score earned / total marks) * 100

Feedback categories:
85 – 100 = Excellent
70 – 84 = Good
50 – 69 = Fair
Below 50 = Poor

FRONTEND INTEGRATION

Frontend can easily use API

Typical student journey:
Login → Save JWT
Fetch questions
Start exam
Display countdown timer
User answers questions
Submit exam
Display grading results

Frontend Suggestions:
React
Next.js
Vue
Flutter
Android
iOS

SCREENSHOTS (included in screenshots folder)

questions_list.jpg – student question fetch view
start_exam.jpg – student starting exam
submit_success.jpg – grading response

AUTHOR

Udeagha Mark Mang
Backend Engineer
Python | Django | Problem Solver