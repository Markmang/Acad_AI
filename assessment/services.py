from django.utils import timezone
from datetime import timedelta
from rest_framework.exceptions import ValidationError
from .models import Submission, Answer
from grading.services import grade_submission
from rest_framework import status


def start_exam(user, exam):
    submission, created = Submission.objects.get_or_create(
        student=user,
        exam=exam
    )

    if submission.is_submitted:
        return {
            "status": "already_submitted",
            "message": "You already completed this exam"
        }, status.HTTP_400_BAD_REQUEST

    if submission.started_at:
        return {
            "status": "already_started",
            "message": "Exam already started"
        }, status.HTTP_200_OK

    submission.started_at = timezone.now()
    submission.save()

    return {
        "status": "started",
        "message": "Exam started successfully",
        "start_time": submission.started_at
    }, status.HTTP_200_OK


def handle_submission(user, exam, answers):
    """
    Handles student exam submission:
    - ensures exam started
    - prevents multiple submissions
    - enforces student-specific time limit
    - saves answers
    - triggers grading
    - returns clean response structure (no crashes)
    """

    submission = Submission.objects.filter(student=user, exam=exam).first()

    # ==============================
    # Exam Not Started
    # ==============================
    if not submission or not submission.started_at:
        return {
            "status": "not_started",
            "message": "You must start the exam before submitting"
        }, status.HTTP_400_BAD_REQUEST

    # ==============================
    # Already Submitted
    # ==============================
    if submission.is_submitted:
        return {
            "status": "already_submitted",
            "message": "You already submitted this exam"
        }, status.HTTP_400_BAD_REQUEST

    # ==============================
    # Time Expired
    # ==============================
    end_time = submission.started_at + timedelta(minutes=exam.duration)

    if timezone.now() > end_time:
        return {
            "status": "time_expired",
            "message": "Time is up! You cannot submit anymore"
        }, status.HTTP_400_BAD_REQUEST

    # ==============================
    # Save Answers
    # ==============================
    for ans in answers:
        Answer.objects.create(
            submission=submission,
            question_id=ans["question"],
            student_answer=ans["answer"]
        )

    # ==============================
    # Grade Submission
    # ==============================
    score, total_marks = grade_submission(submission)

    submission.total_score = score
    submission.submitted_at = timezone.now()
    submission.is_submitted = True
    submission.save()

    return {
        "status": "success",
        "submission": submission,
        "score": score,
        "total_marks": total_marks
    }, status.HTTP_201_CREATED