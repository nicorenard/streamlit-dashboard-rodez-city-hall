questions = [
    {"question": "Quelle est la date qui représente un creux dans la natalité ?",
    "options": ["1916", "1983", "2011"], "answer": "1983"},
    {"question": "Quel est le prénom TOP homme de l'année 1980?",
     "options": ["Jean", "Pierre", "Nicolas", "Sebastien"], "answer": "Nicolas"},
    {"question": "Quelle année à l'espérance de vie la plus faible?",
     "options": ["2013", "2006", "1991", "1979"], "answer": "1991"},
    {"question": "Quelle saison est la moins elevée en terme de déces sur toute la pèriode?",
     "options": ["Printemps", "Automne", "Hiver", "Ete"], "answer": "Automme"},
    {"question": "Quelle année et saison a été le plus marquée par les mariages?",
     "options": ["Automne 1920", "Ete 1946", "Printemps 1969", "Hiver 1977"], "answer": "Printemps 1969"},
    {"question": "Quel a été le plus grand écart d'age du point de vue des mariages ?",
     "options": ["8", "14", "20"], "answer": "20"},

]


def calculate_score(user_answers):
    score = 0
    results = []
    for index, question in enumerate(questions):
        correct_answer = question["answer"]
        user_answer = user_answers[index]
        is_correct = user_answer == correct_answer
        if is_correct:
            score += 1
        results.append({"question": question["question"],
                        "user_answer": user_answer,
                        "correct_answer": correct_answer,
                        "is_correct": is_correct})
    return score, results