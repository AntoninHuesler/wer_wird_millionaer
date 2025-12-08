import sqlite3
import pytest
import repo_game

# ------------------------------------------------------------
# Setup: Temporäre DB für tests
# ------------------------------------------------------------


@pytest.fixture
def temp_db(tmp_path, monkeypatch):
    """
    Legt eine temporäre SQLite-DB mit der gleichen Struktur wie game.db an
    und setzt repo_game.db_game_path auf diese Test-DB.
    """
    db_file = tmp_path / "game_test.db"

    conn = sqlite3.connect(db_file)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS players (
          game_id  INTEGER PRIMARY KEY AUTOINCREMENT,
          username TEXT UNIQUE NOT NULL,
          score    INTEGER NOT NULL DEFAULT 0
        );
        """
    )
    conn.commit()
    conn.close()

    # repo_game so patchen, dass login() die Test-DB benutzt
    monkeypatch.setattr(repo_game, "db_game_path", str(db_file))

    return str(db_file)


# ------------------------------------------------------------
# TDD: Username Validierung
# ------------------------------------------------------------


def test_login_username_validation(temp_db):
    """
    Testet die geplante neue Login Logik:
    - ungültiger Username (kein Buchstabe)
    - neuer gültiger Username
    - bereits vorhandener gültiger Username
    """
    username = "   1234"
    # Ungültiger Username: kein Buchstabe
    created, name, valid = repo_game.login(username)
    assert created is False
    assert name == "   1234"
    assert valid is False

    # sicherstellen, dass ungültiger username  "  1234" nicht in der DB gelandet ist
    conn = sqlite3.connect(temp_db)
    (count_invalid,) = conn.execute(
        "SELECT COUNT(*) FROM players WHERE username = ?;",
        ("1234",),
    ).fetchone()
    conn.close()
    assert count_invalid == 0


# ------------------------------------------------------------
# TEST 1: Username darf nicht empty sein
# ------------------------------------------------------------


def test_login_empty_username(temp_db):
    result = repo_game.login("")
    assert result == (False, "", False)


# ------------------------------------------------------------
# TEST 2: Login bestehender username
# ------------------------------------------------------------


def test_login_existing_username(temp_db):
    username = "hans"

    # User in Test-DB anlegen
    conn = sqlite3.connect(temp_db)
    conn.execute(
        "INSERT INTO players(username, score) VALUES (?, ?);",
        (username, 0),
    )
    conn.commit()
    conn.close()

    # login aufrufen mit User der bereits existiert
    result = repo_game.login(username)
    assert result == (False, username, True)

    # sicherstellen, dass der vorhandene username nicht nochmals in die DB geschrieben wird
    conn = sqlite3.connect(temp_db)
    (count,) = conn.execute(
        "SELECT COUNT(*) FROM players WHERE username = ?;",
        (username,),
    ).fetchone()
    conn.close()
    assert count == 1


# ------------------------------------------------------------
# TEST 3: Login neuer Username
# ------------------------------------------------------------


def test_login_new_username(temp_db):
    username = "peter"

    # login mit neuem username
    result = repo_game.login(username)
    assert result == (True, username, True)

    # prüfen, ob der User wirklich in der DB gelandet ist
    conn = sqlite3.connect(temp_db)
    row = conn.execute(
        "SELECT username, score FROM players WHERE username = ?;",
        (username,),
    ).fetchone()
    conn.close()

    # username stimmt & default-score = 0
    assert row == (username, 0)
