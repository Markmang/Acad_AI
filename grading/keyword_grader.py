# Grades theory questions by matching keywords.
def grade_theory(answer, keywords, marks):
    if not keywords:
        return 0, "No keywords provided"

    score = 0
    matched = []

    for word in keywords:
        if word.lower() in answer.lower():
            matched.append(word)
            score += 1

    percent = (score / len(keywords))
    final_score = percent * marks

    feedback = f"Matched keywords: {matched}" if matched else "Poor answer. No key concepts found"

    return round(final_score, 2), feedback
