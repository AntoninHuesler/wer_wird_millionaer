# Tkinter-Frontend für "Wer wird Millionär"
#
#frontend.py steuert das GUI des Spiels.
# Es kommuniziert mit: 
# - game_logic-py (Spiellogik)
# - repo_game.py (Zugriff auf DB)

import tkinter as tk  # Importiert das Tkinter-Modul für die Oberfläche
import game_logic  # Importiert die Spiellogik
import repo_game  # Importiert die Funktionen für das Ranking


class QuizGUI(tk.Tk):  # Hauptklasse für die Quiz-Oberfläche
    def __init__(self):
        super().__init__()
        self.title("Wer wird Millionär")
        self.geometry("420x350")

        # --- Attribute für Spielzustand ---
        self.username = ""              #Aktueller Benutzername
        self.score = 0                  #Aktueller Punktestand
        self.current_question = None    #Aktuelle Frage
        self.buttons = []               #Liste der Antwort-Buttons

        # --- Startbildschirm aufbauen ---
        self.build_login()


    # --------------------------------------------------------------
    # LOGIN-BEREICH
    # --------------------------------------------------------------
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


    # --------------------------------------------------------------
    # STARTBILDSCHIRM
    # --------------------------------------------------------------
    def build_start_screen(self):  # Anzeige des Start-Bildschirms (Spiel starten)
        self._clear()
        tk.Button(self, text="Spiel starten", command=self.start_game).pack(pady=20)


    # --------------------------------------------------------------
    # SPIELSTART UND FRAGEN-ANSICHT
    # --------------------------------------------------------------
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

        # --- Header für username-Anzeige oben rechts ---
        header = tk.Frame(self)
        header.pack(side="top", fill="x", pady=4)
        tk.Label(
            header,
            text=f"Spieler: {self.username}",
            font=("Arial", 14)
        ).pack(side="right", padx=10)

        # --- Aktuelle Fragenummer & Anz. Fragen gesamt aus Gamestate holen ---
        i = game_logic.GameState["index_current_question"]
        total = len(game_logic.GameState["questions"])
        current_num = i + 1

        # --- Frage & Antworten anzeigen ---
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

        # --- Fusszeile mit Fortschritt & Punktestand ---
        footer = tk.Frame(self)
        footer.pack(side="bottom", fill="x", pady=8)

        # Linke Seite Fusszeile: Fragefortschritt
        tk.Label(
            footer,
            text = f"Frage: {current_num}/{total}",
            font=("Arial", 14)
        ).pack(side="left", padx=10)

        # Rechte Seite Fusszeile: Punktestand
        score = game_logic.GameState["score"]
        tk.Label(
            footer,
            text=f"Punktestand: {score}",
            font=("Arial", 14)
        ).pack(side="right", padx=10)


    # --------------------------------------------------------------
    # ANTWORT-PRÜFUNG UND SPIELFORTSCHRITT
    # --------------------------------------------------------------

    def submit_answer(self, answer_index):  # Prüft gegebene Antwort und zeigt Feedback
        correct, finished, _ = game_logic.submit_answer(answer_index)

        # Buttons nach Klick daktivieren, damit keine Mehrfachantworten möglich sind
        for btn in self.buttons:
            btn.config(state="disabled")

        # Rückmeldung zu gegebener Antwort anzeigen
        msg = "Richtig!" if correct else "Falsch!"
        tk.Label(self, text=msg, font=("Arial", 12)).pack(pady=10)

        # Wenn Antwort falsch oder Spielende erreicht
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


    # --------------------------------------------------------------
    # HILFSFUNKTIONEN
    # --------------------------------------------------------------

    def _clear(self):  # Hilfsfunktion: leert das Fenster
        for widget in self.winfo_children():
            widget.destroy()

    # --------------------------------------------------------------
    # ERGEBNISANZEIGE
    # --------------------------------------------------------------


    def show_result(self, score):  # Anzeige des Endbildschirms mit Score und Ranking
        self._clear()
        tk.Label(
            self, text=f"Spiel vorbei! Dein Score: {score}", font=("Arial", 14)
        ).pack(pady=8)
        # Ranking aus DB holen:

        rank_list = repo_game.get_rank(limit=5)  # Top 5 Spieler holen
        tk.Label(self, text="Top 5 Spieler:", font=("Arial", 12, "bold")).pack(pady=3)

        #Liste Ranking darstellen
        for place, (username, r_score) in enumerate(rank_list, 1):
            tk.Label(
                self, text=f"{place}. {username}: {r_score} Punkte", font=("Arial", 11)
            ).pack()
        #Button für Neustart und Redirect auf Login-Screen

        tk.Button(self, text="Neustart", command=self.build_login).pack(
            pady=15
        )  # Button zum Neustart


if __name__ == "__main__":  # Startet das Quiz-Programm, sobald Datei ausgeführt wird
    QuizGUI().mainloop()  # Hauptloop für das GUI-Fenster starten
