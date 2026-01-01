from django.urls import path
from .views import (
    ExamListCreateView,
    ExamDetailView,
    ExamQuestionsView,
    SubmitExamView,
    AddQuestionView,
    QuestionDetailView,
    ExamSubmissionsView,
    StartExamView    
)

urlpatterns = [
    # STAFF Exams CRUD
    path("", ExamListCreateView.as_view()),
    path("<int:pk>/", ExamDetailView.as_view()),

    # STAFF Question CRUD
    path("<int:exam_id>/questions/add/", AddQuestionView.as_view()),
    path("questions/<int:pk>/", QuestionDetailView.as_view()),

    # STAFF View Submissions
    path("<int:exam_id>/submissions/", ExamSubmissionsView.as_view()),

    #STUDENT Start Exam
    path("<int:exam_id>/start/", StartExamView.as_view()),

    # STUDENT View Questions
    path("<int:exam_id>/questions/", ExamQuestionsView.as_view()),

    # STUDENT Submit Exam
    path("<int:exam_id>/submit/", SubmitExamView.as_view()),
]
