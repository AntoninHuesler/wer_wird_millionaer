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
        return (True, username)
    finally:
        conn.close()


if __name__ == "__main__":
    print(login("maximilam"))
