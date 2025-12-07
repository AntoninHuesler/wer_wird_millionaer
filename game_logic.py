"""Beschreibt die Spiellogik und verwaltet den Spielzustand."""

from repo_question import fetch_12_questions
from repo_game import login, write_score_to_db


# Spielzustand
GAME_STATE = {
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
    result = login(username)  # (created, "username", valid)
    GAME_STATE["username"] = result[1]  # Username aus Rückgabe ins GameState
    return result  # gleiche Rückgabe wie login()


def start_new_game():
    """Startet ein neues Spiel und gibt (text, answers) der ersten Frage zurück."""

    GAME_STATE["questions"] = fetch_12_questions()
    GAME_STATE["index_current_question"] = 0
    GAME_STATE["score"] = 0

    first_text = GAME_STATE["questions"][0][0]
    first_answers = GAME_STATE["questions"][0][1]
    return first_text, first_answers


def submit_answer(answer_index):
    """Prüft Antwort, erhöht Score, rückt ggf. zur nächsten Frage vor."""
    i = GAME_STATE["index_current_question"]
    correct_index = GAME_STATE["questions"][i][2]

    correct = answer_index == correct_index  # True / False
    finished = (not correct) or (i == len(GAME_STATE["questions"]) - 1)  # True / False

    if correct:
        GAME_STATE["score"] += 100
    if finished:
        write_score_to_db(GAME_STATE["username"], GAME_STATE["score"])
    else:
        GAME_STATE["index_current_question"] += 1
    return correct, finished, correct_index  # bool,bool, int


def load_question():
    """Lädt die aktuelle Frage basierend auf index_current_question."""
    i = GAME_STATE["index_current_question"]
    text = GAME_STATE["questions"][i][0]
    answers = GAME_STATE["questions"][i][1]
    return text, answers


#
# if __name__ == "__main__":
