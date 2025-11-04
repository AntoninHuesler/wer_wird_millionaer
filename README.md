# Wer wird Millionär

Ein interaktives Quizspiel im Stil von „Wer wird Millionär“, entwickelt mit Python und Tkinter. Dieses Projekt vereint Wissen, Strategie und Spannung in einer benutzerfreundlichen Oberfläche. Teste dein Allgemeinwissen, klettere die Gewinnstufen empor und sichere dir einen Platz im Highscore!

Die App enthält einfache Eingabe- und Auswahlfunktionen, ein klares Punktesystem und eine visuelle Darstellung deines Fortschritts im Spiel.

## Features

* Klassisches Quiz-Gameplay: Beantworte 12 Fragen mit steigendem Schwierigkeitsgrad (je 4x leicht, mittel, schwer).
* Grafische Oberfläche: Eine intuitive und saubere Benutzeroberfläche, erstellt mit Tkinter.
* Spieler-Ranking: Ein Highscore-System, das deine besten Runden speichert.

## Getting Started
Folge diesen Schritten, um das Spiel auf deinem lokalen Rechner einzurichten und zu starten.

### Voraussetzungen

* Python 3.x
* Das `sqlite3` Command-Line-Tool (ist normalerweise bei Python standardmässig dabei).

### Installation & Einrichtung

1.  Klone dieses Repository auf deinen Computer.
2.  Öffne ein Terminal und navigiere in das Projektverzeichnis.

### Spiel starten

Sobald die Einrichtung abgeschlossen ist, kannst du das Spiel starten:

```bash
python frontend.py
```

## Spielablauf

1.  Login: Starte das Spiel (`python frontend.py`). Du wirst aufgefordert, deinen Benutzernamen einzugeben.
2.  Spielstart: Klicke auf "Spiel starten", um deine Runde zu beginnen.
3.  Fragen: Dir werden nacheinander 12 Fragen gestellt. Wähle die korrekte Antwort aus und bestätige sie.
4.  Auswertung: Nach jeder Antwort erhältst du sofort Feedback.
5. Spielende: Sobald du alle Fragen beantwortet oder eine falsch beantwortet hast, ist das Spiel vorbei.
6. Ranking: Dein Score wird gespeichert und du kannst deinen Platz im globalen Ranking einsehen.

## Projektarchitektur

Dieses Projekt nutzt eine klare Trennung von Verantwortlichkeiten, um die Wartbarkeit und Übersichtlichkeit zu gewährleisten. Die Kernidee war, die Anzeige (GUI), die Spiellogik und den Datenzugriff voneinander zu entkoppeln.

* `frontend.py`: Startpunkt / GUI-Logik (Tkinter)
* `game_logic.py`: Spiellogik, steuert den gesamten Spielablauf
* `repo_question.py`: Datenzugriff auf die Fragen-Datenbank
* `repo_game.py`: Datenzugriff auf die Spieler- & Score-Datenbank
* `data/questions.db`: Datenbank mit allen Quizfragen
* `data/game.db`: Datenbank für Spieler-Logins und Highscores
* `data/*.sql`: SQL-Skripte für Setup, Seed und Reset der DBs

## Entwicklung & Tests

### Tests

Das Projekt verwendet das `unittest`-Modul von Python für Unit-Tests.

### Stilregeln

Wir verwenden flake8 zur Sicherstellung der Code-Qualität. Anstatt den gesamten PEP 8-Standard durchzusetzen, verwenden wir eine spezifische Auswahl von Regeln, die in der `setup.cfg` definiert sind.

### Datenbank-Reset
Wenn du die Spielstände und Spieler zurücksetzen möchtest, ohne die Fragen anzutasten, kannst du folgendes Skript ausführen:

```bash
sqlite3 data/game.db < data/004_clear_game.sql
```

## Lizenz

Siehe die `LICENSE`-Datei im Projekt für Details.

