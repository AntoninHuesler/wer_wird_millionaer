import sqlite3
from pathlib import Path

db_game_path = Path("data/game.db")  # Pfad zur Datenbank questions.db


def login(username: str):
    """
    Prüft, ob der Username in game.db/players existiert.
    - Falls leerer Username → (False, username)
    - Falls vorhanden → (False, username)
    - Falls neu → Eintrag anlegen und (True, username)
    """
    if username == "":
        return (False, username)

    conn = sqlite3.connect(db_game_path)
    try:
        # Existenz prüfen
        cursor = conn.execute(
            "SELECT 1 FROM players WHERE username = ? LIMIT 1;", (username,)
        )
        if cursor.fetchone() is not None:
            return (False, username)

        # Neu eintragen
        conn.execute("INSERT INTO players(username) VALUES (?);", (username,))
        conn.commit()
        user = username
        return (True, username)
    finally:
        conn.close()


def write_score_to_db(username, score):
    """Speichert den Score eines Users."""
    with sqlite3.connect(db_game_path) as conn:
        conn.execute(
            "UPDATE players SET score = ? WHERE username = ?;", (score, username)
        )
        conn.commit()


def get_rank(limit=5):
    """Gibt Top-`limit` als Liste (username, score) zurück."""
    with sqlite3.connect(db_game_path) as conn:
        rows = conn.execute(
            "SELECT username, score FROM players "
            "ORDER BY score DESC, username ASC LIMIT ?;",
            (limit,),
        ).fetchall()
    return [(r[0], r[1]) for r in rows]


if __name__ == "__main__":
    print(get_rank())
