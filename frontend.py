# Tkinter für Frontend

import tkinter as tk  # Importiert das Tkinter-Modul für die Oberfläche
import game_logic  # Importiert die Spiellogik
import repo_game  # Importiert die Funktionen für das Ranking


class QuizGUI(tk.Tk):  # Hauptklasse für die Quiz-Oberfläche
    def __init__(self):
        super().__init__()
        self.title("Wer wird Millionär")
        self.geometry("420x350")
        self.username = ""
        self.score = 0
        self.current_question = None
        self.buttons = []
        self.build_login()

    def build_login(self):  # Anzeige des Login-Bildschirms
        self._clear()  # Fenster leeren
        tk.Label(self, text="Benutzername:").pack(pady=10)
        entry = tk.Entry(self)
        entry.pack()
        tk.Button(self, text="Login", command=lambda: self.login(entry.get())).pack(
            pady=10
        )

    def login(self, username):  # Login-Funktion für Benutzer
        success, _ = game_logic.do_login(
            username
        )  # Prüft, ob Username in Datenbank existiert
        self.username = username  # Benutzername speichern
        if success:
            self.build_start_screen()
        else:
            tk.Label(self, text="Login fehlgeschlagen!").pack()

    def build_start_screen(self):  # Anzeige des Start-Bildschirms (Spiel starten)
        self._clear()
        tk.Button(self, text="Spiel starten", command=self.start_game).pack(pady=20)

    def start_game(self):  # Startet das Spiel, lädt erste Frage
        question_text, answers = (
            game_logic.start_new_game()
        )  # Neue Frage + Antworten holen
        self.score = 0  # Score zurücksetzen
        self.current_question = [question_text, answers]  # Frage für Anzeige speichern
        self.build_question_screen()

    def build_question_screen(
        self,
    ):  # Zeigt die aktuelle Quiz-Frage mit Antwortmöglichkeiten
        self._clear()
        question_text, answers = self.current_question
        tk.Label(self, text=question_text, font=("Arial", 15)).pack(
            pady=15
        )  # Frage anzeigen
        self.buttons = []  # Buttons für Antworten
        for i, answer in enumerate(answers):
            btn = tk.Button(
                self,
                text=answer,
                width=25,
                command=lambda idx=i: self.submit_answer(idx),  # Antwort wird übergeben
            )
            btn.pack(pady=5)
            self.buttons.append(btn)

    def submit_answer(self, answer_index):  # Prüft gegebene Antwort und zeigt Feedback
        correct, finished, _ = game_logic.submit_answer(answer_index)
        for btn in self.buttons:
            btn.config(state="disabled")
        msg = "Richtig!" if correct else "Falsch!"
        tk.Label(self, text=msg, font=("Arial", 12)).pack(pady=10)

        if not correct:
            # Bei falscher Antwort: Endscreen + Ranking anzeigen
            self.show_result(game_logic.GameState["score"])
            return

        if finished:
            # Wenn alle Fragen beantwortet: Endscreen + Ranking zeigen
            self.show_result(game_logic.GameState["score"])
        else:
            # Sonst: nächste Frage nach kurzer Wartezeit anzeigen
            def next():
                text, answers = game_logic.load_question()
                self.current_question = [text, answers]
                self.build_question_screen()

            self.after(1200, next)  # 1,2 Sekunden später geht's weiter

    def _clear(self):  # Hilfsfunktion: leert das Fenster
        for widget in self.winfo_children():
            widget.destroy()

    def show_result(self, score):  # Anzeige des Endbildschirms mit Score und Ranking
        self._clear()
        tk.Label(
            self, text=f"Spiel vorbei! Dein Score: {score}", font=("Arial", 14)
        ).pack(pady=8)
        rank_list = repo_game.get_rank(limit=5)  # Top 5 Spieler holen
        tk.Label(self, text="Top 5 Spieler:", font=("Arial", 12, "bold")).pack(pady=3)
        for place, (username, r_score) in enumerate(rank_list, 1):
            tk.Label(
                self, text=f"{place}. {username}: {r_score} Punkte", font=("Arial", 11)
            ).pack()
        tk.Button(self, text="Neustart", command=self.build_login).pack(
            pady=15
        )  # Button zum Neustart


if __name__ == "__main__":  # Startet das Quiz-Programm, sobald Datei ausgeführt wird
    QuizGUI().mainloop()  # Hauptloop für das GUI-Fenster starten
