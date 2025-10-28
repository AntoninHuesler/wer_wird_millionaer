import sqlite3
from pathlib import Path

db_questions_path = Path(__file__).resolve().parent / "data" / "questions.db"


def pick(
    diff: str, n: int = 4
):  # Funktion holt n Fragen (Default = 4) einer Schwierigkeit (diff)
    with sqlite3.connect(db_questions_path) as conn:  # verbindung zu questions.db
        # Führt SQL Abfrage aus
        rows = conn.execute(
            """     
            SELECT text, answer_a, answer_b, answer_c, answer_d, correct_index
            FROM questions
            WHERE difficulty = ?
            ORDER BY RANDOM() 
            LIMIT ?;
        """,
            (diff, n),
        ).fetchall()  # übergibt parameter diff & n den ?
    # baut aus jeder Zeile der db ein Tupel: (Fragetext, [Antwort A, Antwort B...], korrekterIndex)
    return [(r[0], [r[1], r[2], r[3], r[4]], r[5]) for r in rows]


def fetch_12_questions():  # führt die funktin pick 4 mal aus mit den drei verschiedenen Schwierigkeiten
    qs = pick("leicht", 4) + pick("mittel", 4) + pick("schwer", 4)
    return qs


if __name__ == "__main__":
    print(fetch_12_questions())
