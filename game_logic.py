from repo_question import fetch_12_questions

# Globaler Spielzustand
GameState = {
    "questions": [],  # Liste aus {text, answers, correct_index}
    "index_current_question": 0,
    "score": 0,
}


def start_new_game():
    """Startet ein neues Spiel und gibt (text, answers) der ersten Frage zurück."""
    global GameState
    GameState = {"questions": [], "index_current_question": 0, "score": 0}

    raw_questions = fetch_12_questions()

    # nutzt DEINE fetch_12_questions()
    GameState["questions"] = fetch_12_questions()

    first_text = GameState["questions"][0][0]
    first_answers = GameState["questions"][0][1]
    return first_text, first_answers


if __name__ == "__main__":
    print(start_new_game())
    print(GameState)
