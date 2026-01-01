from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import generics
from django.shortcuts import get_object_or_404
from .models import Exam, Question, Submission
from .serializers import (
    QuestionSerializer,
    SubmissionSerializer,
    ExamSerializer,
    QuestionCreateSerializer
)
from .permissions import IsExamOwner
from .services import handle_submission, start_exam
from rest_framework import status
from .serializers import RegisterSerializer


# =========================
# STUDENT VIEWS
# =========================

class ExamQuestionsView(APIView):
    """
    Students view questions in an exam
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, exam_id):
        exam = get_object_or_404(Exam, id=exam_id)
        questions = exam.questions.all()
        data = QuestionSerializer(questions, many=True).data
        return Response(data)

class SubmitExamView(generics.GenericAPIView):
    """
    Students submit exam + get graded feedback
    Browsable + JSON friendly + includes full exam summary feedback
    """
    permission_classes = [IsAuthenticated]
    serializer_class = SubmissionSerializer
    queryset = Exam.objects.all()   # REQUIRED by GenericAPIView

    def get(self, request, exam_id):
        """
        Enable browsable API form instead of GET 405
        """
        serializer = self.get_serializer()
        return Response(serializer.data)

    def post(self, request, exam_id):
        exam = get_object_or_404(Exam, id=exam_id)

        # Validate incoming payload
        serializer = self.get_serializer(
            data=request.data,
            context={"exam": exam}
        )
        serializer.is_valid(raise_exception=True)

        # ==============================
        # Handle submission + grading
        # ==============================
        result, http_status = handle_submission(
            request.user,
            exam,
            serializer.validated_data["answers"]
        )

        # If submission failed (not started, expired, already submitted, etc)
        if result["status"] != "success":
            return Response(result, status=http_status)

        # If success, extract values
        submission = result["submission"]
        score = result["score"]
        total_marks = result["total_marks"]
        percentage = round((score / total_marks) * 100, 2)

        # ===============================
        # EXAM WIDE FEEDBACK SUMMARY
        # ===============================
        if percentage >= 85:
            exam_feedback = "Excellent performance! You demonstrated strong understanding."
        elif percentage >= 70:
            exam_feedback = "Good job! You have a solid grasp but there is room for improvement."
        elif percentage >= 50:
            exam_feedback = "Fair attempt. Revise the weak areas and try again."
        else:
            exam_feedback = "Poor performance. You need to study more and retry."

        return Response(
            {
                "message": "Submission successful",
                "total_score": score,
                "total_marks": total_marks,
                "percentage": percentage,
                "exam_feedback": exam_feedback,
                "answers": [
                    {
                        "question": a.question.text,
                        "student_answer": a.student_answer,
                        "score": a.score_awarded,
                        "feedback": a.feedback,
                    }
                    for a in submission.answers.all()
                ],
            },
            status=status.HTTP_201_CREATED,
        )

# =========================
# STAFF EXAM CRUD
# =========================

class ExamListCreateView(generics.ListCreateAPIView):
    """
    GET  -> list exams (everyone logged in)
    POST -> create exam (staff only)
    """
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ExamDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve / Update / Delete exams
    Only exam owner staff can manage
    """
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    permission_classes = [IsAdminUser, IsExamOwner]

    def perform_update(self, serializer):
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        exam = self.get_object()
        exam.delete()
        return Response({"message": "Exam deleted"})



# =========================
# STAFF QUESTION CRUD
# =========================

class AddQuestionView(generics.CreateAPIView):
    """
    Staff add question to an exam they own
    """
    queryset = Question.objects.all()
    permission_classes = [IsAdminUser, IsExamOwner]
    serializer_class = QuestionCreateSerializer

    def perform_create(self, serializer):
        exam = get_object_or_404(Exam, id=self.kwargs["exam_id"])
        self.check_object_permissions(self.request, exam)
        serializer.save(exam=exam)

class QuestionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Update / Delete question
    Only exam owner staff
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAdminUser]

    def check_object_permissions(self, request, obj):
        exam = obj.exam
        IsExamOwner().has_object_permission(request, self, exam)
        return super().check_object_permissions(request, obj)


# =========================
# STAFF VIEW SUBMISSIONS
# =========================

class ExamSubmissionsView(APIView):
    """
    Staff view all submissions for their exam
    """
    permission_classes = [IsAdminUser, IsExamOwner]

    def get(self, request, exam_id):
        exam = get_object_or_404(Exam, id=exam_id)
        self.check_object_permissions(request, exam)

        submissions = Submission.objects.filter(exam=exam)

        data = [
            {
                "student": s.student.username,
                "score": s.total_score,
                "submitted_at": s.submitted_at
            } for s in submissions
        ]

        return Response(data)

class RegisterView(generics.GenericAPIView):
    """
    Public Student Registration
    Browsable + Returns JWT
    """
    permission_classes = []
    authentication_classes = []
    serializer_class = RegisterSerializer

    def get(self, request):
        """
        Enable browsable API HTML form
        """
        serializer = self.get_serializer()
        return Response(serializer.data)

    def post(self, request):
        """
        Handle actual registration
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        tokens = serializer.get_tokens_for_user(user)

        return Response(
            {
                "message": "Account created successfully",
                "user": {
                    "username": user.username,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name
                },
                "tokens": tokens
            },
            status=status.HTTP_201_CREATED
        )
    
class StartExamView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, exam_id):
        exam = get_object_or_404(Exam, id=exam_id)

        result, code = start_exam(request.user, exam)

        return Response(result, status=code)
