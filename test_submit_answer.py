import game_logic
from unittest.mock import patch


def setup_test_state():
    """Hilfsfunktion zum Zurücksetzen des GAME_STATE für jeden Test."""
    game_logic.GAME_STATE = {
        "username": "TestUser",
        "score": 0,
        "index_current_question": 0,
        "questions": [
            ("Frage 1", ["A", "B", "C", "D"], 2),  # correct_index = 2
            ("Frage 2", ["A", "B", "C", "D"], 1),  # correct_index = 1
        ],
    }


# ------------------------------------------------------------
# TEST 1 – Richtige Antwort (nicht letzte Frage)
# ------------------------------------------------------------
@patch("game_logic.write_score_to_db")
def test_submit_answer_correct(mock_write):
    setup_test_state()

    correct, finished, correct_index = game_logic.submit_answer(2)

    assert correct is True
    assert finished is False
    assert correct_index == 2
    assert game_logic.GAME_STATE["score"] == 100
    assert game_logic.GAME_STATE["index_current_question"] == 1
    mock_write.assert_not_called()


# ------------------------------------------------------------
# TEST 2 – Falsche Antwort
# ------------------------------------------------------------
@patch("game_logic.write_score_to_db")
def test_submit_answer_wrong(mock_write):
    setup_test_state()

    correct, finished, correct_index = game_logic.submit_answer(1)  # correct is 2

    assert correct is False
    assert finished is True
    assert correct_index == 2
    assert game_logic.GAME_STATE["score"] == 0
    mock_write.assert_called_once_with("TestUser", 0)


# ------------------------------------------------------------
# TEST 3 – Letzte Frage richtig beantwortet
# ------------------------------------------------------------
@patch("game_logic.write_score_to_db")
def test_submit_answer_last_question(mock_write):
    setup_test_state()
    game_logic.GAME_STATE["index_current_question"] = 1  # wir stehen auf letzter Frage

    correct, finished, correct_index = game_logic.submit_answer(1)  # richtige Antwort

    assert correct is True
    assert finished is True
    assert correct_index == 1
    assert game_logic.GAME_STATE["score"] == 100
    mock_write.assert_called_once_with("TestUser", 100)
