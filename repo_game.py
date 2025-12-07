"""Datenbank-Operationen für das Spiel."""

import sqlite3
from pathlib import Path

db_game_path = Path(__file__).resolve().parent / "data" / "game.db"


def login(username: str):
    """
    Rückgabe: (created, username, valid)

    einfache Regel: Username muss mindestens einen Buchstaben enthalten und nicht leer sein

    - Ungültiger Username (kein Buchstabe oder leer)
        → (False, username, False)
    - Username bereits vorhanden
        → (False, username, True)
    - Username neu (wird angelegt)
        → (True,  username, True)
    """

    # Validierung: username muss mindestens einen Buchstaben und nicht leer

    if username == "" or not any(ch.isalpha() for ch in username):
        return (False, username, False)

    conn = sqlite3.connect(db_game_path)
    try:
        # Existenz prüfen
        cursor = conn.execute(
            "SELECT 1 FROM players WHERE username = ? LIMIT 1;", (username,)
        )
        if cursor.fetchone() is not None:
            return (False, username, True)

        # Neu eintragen
        conn.execute("INSERT INTO players(username) VALUES (?);", (username,))
        conn.commit()
        return (True, username, True)
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
