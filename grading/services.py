from grading.keyword_grader import grade_theory
from assessment.models import Answer

# automated grading of student submissions.
def grade_submission(submission):
    exam = submission.exam
    questions = exam.questions.all()

    total_marks = sum(q.marks for q in questions)
    score = 0

    # Get answers student submitted
    submitted_answers = {a.question_id: a for a in submission.answers.all()}

    # Loop through every question in the exam
    for question in questions:

        # Student answered this question
        if question.id in submitted_answers:
            ans = submitted_answers[question.id]

            # ---------- MCQ ----------
            if question.question_type == "MCQ":
                if ans.student_answer.strip().lower() == str(question.correct_answer).strip().lower():
                    ans.score_awarded = question.marks
                    ans.feedback = "Correct answer"
                else:
                    ans.score_awarded = 0
                    ans.feedback = f"Incorrect. Correct answer is: {question.correct_answer}"

            # ---------- THEORY ----------
            else:
                score_awarded, feedback = grade_theory(
                    ans.student_answer,
                    question.expected_keywords,
                    question.marks
                )

                ans.score_awarded = score_awarded
                ans.feedback = (
                    feedback +
                    f" | Expected points/keywords: {question.expected_keywords}"
                    if question.expected_keywords else feedback
                )

            ans.save()
            score += ans.score_awarded

        else:
            # Student did NOT answer → create zero-score answer
            Answer.objects.create(
                submission=submission,
                question=question,
                student_answer="",
                score_awarded=0,
                feedback="No answer submitted"
            )

    submission.total_score = score
    submission.save()

    return score, total_marks
