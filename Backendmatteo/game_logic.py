from dataclasses import dataclass
from typing import List, Tuple
from datetime import datetime
import random

# --- Datenklassen (DTOs) ---

@dataclass
class QuestionDTO:
    id: int
    text: str
    answers: List[str]
    correct_index: int
    difficulty: str

@dataclass
class GameState:
    score: int
    current_question_nr: int

@dataclass
class Game:
    id: int
    username: str
    score: int = 0
    questions_asked: List[int] = None
    is_over: bool = False
    start_time: datetime = None
    end_time: datetime = None

    def __post_init__(self):
        if self.questions_asked is None:
            self.questions_asked = []
        if self.start_time is None:
            self.start_time = datetime.now()

    def get_duration(self) -> float:
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        else:
            return 0.0

@dataclass
class LeaderboardEntryDTO:
    username: str
    score: int
    timestamp_duration: float
    rank: int

# --- Beispiel-Fragen ---
QUESTIONS = [
    QuestionDTO(1, "Was ist 2 + 2?", ["1", "2", "3", "4"], 3, "EASY"),
    QuestionDTO(2, "Welche Farbe hat der Himmel?", ["Rot", "Blau", "Grün", "Gelb"], 1, "EASY"),
    QuestionDTO(3, "Wer erfand die Relativitätstheorie?", ["Newton", "Einstein", "Tesla", "Darwin"], 1, "MEDIUM"),
    QuestionDTO(4, "Wie viele Planeten hat das Sonnensystem?", ["7", "8", "9", "10"], 1, "MEDIUM"),
    QuestionDTO(5, "Welches Element hat das Symbol 'Fe'?", ["Eisen", "Fluor", "Silber", "Blei"], 0, "HARD"),
    QuestionDTO(6, "Was ist die Wurzel aus 81?", ["7", "8", "9", "10"], 2, "HARD"),
]

# --- Gespeicherte Spiele (Simulierte DB) ---
SAVED_GAMES = [
    Game(id=1, username="Anna", score=8),
    Game(id=2, username="Ben", score=10),
    Game(id=3, username="Clara", score=7),
    Game(id=4, username="Dieter", score=5),
    Game(id=5, username="Eva", score=9),
]

# --- Funktionen ---

def get_next_question(game: Game) -> Tuple[GameState, QuestionDTO]:
    if game.is_over or len(game.questions_asked) >= 12:
        game.is_over = True
        game.end_time = datetime.now()
        raise Exception("Spiel ist beendet oder alle 12 Fragen wurden gestellt.")

    difficulty_curve = ["EASY"] * 2 + ["MEDIUM"] * 3 + ["HARD"] * 7
    next_difficulty = difficulty_curve[len(game.questions_asked)]

    available_questions = [
        q for q in QUESTIONS
        if q.difficulty == next_difficulty and q.id not in game.questions_asked
    ]

    if not available_questions:
        game.is_over = True
        game.end_time = datetime.now()
        raise Exception(f"Keine weiteren {next_difficulty}-Fragen verfügbar.")

    question = random.choice(available_questions)
    game.questions_asked.append(question.id)

    game_state = GameState(
        score=game.score,
        current_question_nr=len(game.questions_asked)
    )

    return game_state, question

def get_leaderboard(username: str, limit: int = 3) -> Tuple[List[LeaderboardEntryDTO], LeaderboardEntryDTO]:
    sorted_games = sorted(SAVED_GAMES, key=lambda g: g.score, reverse=True)
    top_n = sorted_games[:limit]

    leaderboard = []
    for rank, game in enumerate(top_n, start=1):
        leaderboard.append(LeaderboardEntryDTO(
            username=game.username,
            score=game.score,
            timestamp_duration=game.get_duration(),
            rank=rank
        ))

    own_game = next((g for g in sorted_games if g.username == username), None)
    if own_game:
        own_rank = sorted_games.index(own_game) + 1
        own_entry = LeaderboardEntryDTO(
            username=own_game.username,
            score=own_game.score,
            timestamp_duration=own_game.get_duration(),
            rank=own_rank
        )
    else:
        own_entry = None

    return leaderboard, own_entry

# --- Beispiel für den Programmablauf ---

if __name__ == "__main__":
    # Beispiel: Neues Spiel starten
    game = Game(id=10, username="Clara")

    try:
        while True:
            state, question = get_next_question(game)
            print(f"Frage {state.current_question_nr}: {question.text}")
            print(f"Antworten: {question.answers}")
            # Hier könntest du Input abfragen, Score erhöhen, etc.
            # Zum Testen überspringen wir die Eingabe
    except Exception as e:
        print(e)

    # Spielende -> Score zufällig simulieren (zum Testen)
    game.score = random.randint(0, 12)
    game.is_over = True
    game.end_time = datetime.now()

    # Spiel in SAVED_GAMES speichern oder aktualisieren
    SAVED_GAMES.append(game)

    # Leaderboard anzeigen
    leaderboard, own_entry = get_leaderboard(game.username, limit=3)

    print("\nTop 3 Leaderboard:")
    for entry in leaderboard:
        print(f"{entry.rank}. {entry.username} - {entry.score} Punkte - Dauer: {entry.timestamp_duration:.1f} Sek.")

    if own_entry:
        print(f"\nDein Rang: {own_entry.rank}, Score: {own_entry.score}, Dauer: {own_entry.timestamp_duration:.1f} Sek.")
    else:
        print("\nDu bist nicht in der Bestenliste.")

