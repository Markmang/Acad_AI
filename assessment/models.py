from django.db import models
from django.contrib.auth.models import User

QUESTION_TYPES = (
    ("MCQ", "Multiple Choice"),
    ("THEORY", "Theory"),
)

class Exam(models.Model):
    title = models.CharField(max_length=255)
    course = models.CharField(max_length=255)
    duration = models.IntegerField()  # minutes
    metadata = models.JSONField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    exam = models.ForeignKey(Exam, related_name="questions", on_delete=models.CASCADE)
    text = models.TextField()
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES)
    marks = models.IntegerField(default=1)

    # MCQ
    options = models.JSONField(null=True, blank=True)
    correct_answer = models.CharField(max_length=255, null=True, blank=True)

    # THEORY
    expected_keywords = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.text

class Submission(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    
    started_at = models.DateTimeField(null=True, blank=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    
    total_score = models.FloatField(default=0)
    is_submitted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('student', 'exam')# Prevent multiple submission

    def __str__(self):
        return f"{self.student} - {self.exam}"



class Answer(models.Model):
    submission = models.ForeignKey(Submission, related_name="answers", on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    student_answer = models.TextField()
    score_awarded = models.FloatField(default=0)
    feedback = models.TextField(null=True, blank=True)
