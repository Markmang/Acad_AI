from rest_framework import serializers
from .models import Exam, Question, Submission, Answer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User

class QuestionSerializer(serializers.ModelSerializer):
    """
    Serializer for exposing exam questions to students.

    This serializer ensures students only receive allowed information
    about each question while hiding sensitive internal fields such as
    correct answers or grading logic.

    Returned fields include:
    • id:                 unique question identifier
    • text:               question content
    • question_type:      (MCQ / THEORY)
    • marks:              marks allocated
    • options:            list of selectable options (for MCQ only)

    This design supports:
    • Browsable API friendliness
    • Clear frontend consumption
    • Secure question delivery
    """
    class Meta:
        model = Question
        fields = ["id", "text", "question_type", "marks", "options"]


class AnswerInputSerializer(serializers.Serializer):
    """
    Represents a single student answer in a submission.

    Fields:
    • question:    question ID being answered
    • answer:      student's answer value
                  (Dropdown value for MCQ, text for THEORY)
    """
    question = serializers.IntegerField()
    answer = serializers.CharField()


class SubmissionSerializer(serializers.Serializer):
    """
    Serializer for validating student exam submissions.
    • Ensures submitted questions belong to the selected exam
    • Prevents tampering or answering unrelated questions
    • Enforces MCQ option validation
      (students can only submit predefined options)
    • Supports DRF browsable API behavior:
        - MCQ -> dropdown selection
        - THEORY -> free text input

    This guarantees only valid and secure data reaches
    the grading engine and business logic layer.
    """
    answers = AnswerInputSerializer(many=True)

    def validate(self, data):
        exam = self.context["exam"]
        questions = exam.questions.all()
        question_map = {q.id: q for q in questions}

        for ans in data["answers"]:
            q = question_map.get(ans["question"])

            if not q:
                raise serializers.ValidationError("Invalid question")

            # Prevent invalid MCQ answers
            if q.question_type == "MCQ":
                if ans["answer"] not in q.options:
                    raise serializers.ValidationError(
                        f"Answer must be one of {q.options}"
                    )
        return data

class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = [
            "id",
            "title",
            "course",
            "duration",
            "metadata",
            "created_by",
            "created_at"
        ]
        read_only_fields = ["created_by", "created_at"]

class QuestionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            "id",
            "text",
            "question_type",
            "marks",
            "options",
            "correct_answer",
            "expected_keywords",
        ]
        read_only_fields = ["id"]
    def validate(self, data):
        if data["question_type"] == "MCQ":
            if not data.get("options"):
                raise serializers.ValidationError("MCQ questions must include options")
            if not data.get("correct_answer"):
                raise serializers.ValidationError("MCQ must have a correct answer")
        return data

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "first_name",
            "last_name"
        ]

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already taken")
        return value

    def validate_email(self, value):
        if value and User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already in use")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=validated_data["password"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", "")
        )

        user.is_staff = False #only students can create account
        user.is_superuser = False
        user.is_active = True
        user.save()

        return user

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }# users get token on signup