from repo_question import fetch_12_questions
from repo_game import login
from repo_game import write_score_to_db

# Spielzustand
GameState = {
    "username": "",
    "questions": [],  # Liste aus {text, answers, correct_index}
    "index_current_question": 0,
    "score": 0,
}


def do_login(username):
    """
    Ruft login() auf, speichert den Username im GameState
    und gibt das gleiche zurück wie login().
    """
    result = login(username)  # z. B. (True, "antonin")
    GameState["username"] = result[1]  # Username aus Rückgabe ins GameState
    return result  # exakt gleiche Rückgabe wie login()


def start_new_game():
    """Startet ein neues Spiel und gibt (text, answers) der ersten Frage zurück."""

    GameState["questions"] = fetch_12_questions()
    GameState["index_current_question"] = 0
    GameState["score"] = 0

    first_text = GameState["questions"][0][0]
    first_answers = GameState["questions"][0][1]
    return first_text, first_answers


def submit_answer(answer_index):
    """Prüft Antwort, erhöht Score, rückt ggf. zur nächsten Frage vor."""
    i = GameState["index_current_question"]
    correct_index = GameState["questions"][i][2]

    correct = answer_index == correct_index  # True / False
    finished = (not correct) or (i == len(GameState["questions"]) - 1)  # True / False

    if correct:
        GameState["score"] += 100
    if finished:
        write_score_to_db(GameState["username"], GameState["score"])
    else:
        GameState["index_current_question"] += 1
    return correct, finished, correct_index  # bool,bool, int


def load_question():
    """Lädt die aktuelle Frage basierend auf index_current_question."""
    i = GameState["index_current_question"]
    text = GameState["questions"][i][0]
    answers = GameState["questions"][i][1]
    return text, answers


#
# if __name__ == "__main__":
