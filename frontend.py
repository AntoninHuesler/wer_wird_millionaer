# Tkinter für Frontend

import tkinter as tk
import game_logic


class QuizGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Wer wird Millionär")
        self.geometry("420x350")
        self.username = ""
        self.score = 0
        self.current_question = None
        self.buttons = []
        self.build_login()

    def build_login(self):
        self._clear()
        tk.Label(self, text="Benutzername:").pack(pady=10)
        entry = tk.Entry(self)
        entry.pack()
        tk.Button(self, text="Login", command=lambda: self.login(entry.get())).pack(
            pady=10
        )

    def login(self, username):
        success, _ = game_logic.do_login(username)
        self.username = username
        if success:
            self.build_start_screen()
        else:
            tk.Label(self, text="Login fehlgeschlagen!").pack()

    def build_start_screen(self):
        self._clear()
        tk.Button(self, text="Spiel starten", command=self.start_game).pack(pady=20)

    def start_game(self):
        question_text, answers = game_logic.start_new_game()
        self.score = 0
        self.current_question = [question_text, answers]
        self.build_question_screen()

    def build_question_screen(self):
        self._clear()
        question_text, answers = self.current_question
        tk.Label(self, text=question_text, font=("Arial", 15)).pack(pady=15)
        self.buttons = []
        for i, answer in enumerate(answers):
            btn = tk.Button(
                self,
                text=answer,
                width=25,
                command=lambda idx=i: self.submit_answer(idx),
            )
            btn.pack(pady=5)
            self.buttons.append(btn)

    def submit_answer(self, answer_index):
        correct, finished, _ = game_logic.submit_answer(answer_index)
        for btn in self.buttons:
            btn.config(state="disabled")
        msg = "Richtig!" if correct else "Falsch!"
        tk.Label(self, text=msg, font=("Arial", 12)).pack(pady=10)
        if finished:
            tk.Label(
                self,
                text=f"Spiel beendet! Dein Punktestand: {game_logic.GameState['score']}",
                font=("Arial", 13),
            ).pack(pady=10)
            tk.Button(self, text="Neustart", command=self.build_start_screen).pack(
                pady=10
            )
        else:

            def next():
                text, answers = game_logic.load_question()
                self.current_question = [text, answers]
                self.build_question_screen()

            self.after(1200, next)

    def _clear(self):
        for widget in self.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    QuizGUI().mainloop()
