"""
This is the suggested main entry Python source file for your project
"""

import tkinter as tk
from repo_question import fetch_12_questions


# class QuizFrage:
#   def __init__(self, frage, antworten, richtig, kategorie=None, schwierigkeit=None): # KAtegorie muss noch entfern werden
#       self.frage = frage
#       self.antworten = antworten
#       self.richtig = richtig
#      #self.kategorie = kategorie
#      self.schwierigkeit = schwierigkeit

#  def ist_richtig(self, index):
#     return index == self.richtig


# Eine Instanz der Klasse
# frage1 = QuizFrage(
#   "Wie heißt die Hauptstadt von Frankreich?",
#   ["Berlin", "Paris", "Rom", "Madrid"],
#   1,
#   kategorie="Geographie",
#  schwierigkeit="leicht",
# )


class QuizFrage:
    def __init__(self, frage, antworten, richtig):
        self.frage = frage
        self.antworten = antworten
        self.richtig = richtig

    def ist_richtig(self, index):
        return index == self.richtig


class QuizGUI:
    def __init__(self, root, fragen):
        self.root = root
        self.fragen = fragen
        self.aktuelle_frage_index = 0
        self.punkte = 0

        self.frage_label = tk.Label(root, text="", font=("Arial", 16))
        self.frage_label.pack(pady=20)

        self.antwort_buttons = []
        for i in range(4):
            btn = tk.Button(
                root, text="", width=20, command=lambda i=i: self.antwort_geklickt(i)
            )
            btn.pack(pady=5)
            self.antwort_buttons.append(btn)

        self.ergebnis_label = tk.Label(root, text="", font=("Arial", 14))
        self.ergebnis_label.pack(pady=20)

        self.zeige_frage()

    def zeige_frage(self):
        frage = self.fragen[self.aktuelle_frage_index]
        self.frage_label.config(text=frage.frage)
        for i, antwort in enumerate(frage.antworten):
            self.antwort_buttons[i].config(text=antwort, state="normal")
        self.ergebnis_label.config(text="")

    def antwort_geklickt(self, index):
        frage = self.fragen[self.aktuelle_frage_index]
        if frage.ist_richtig(index):
            self.punkte += 100
            self.ergebnis_label.config(text="Richtig!")
        else:
            self.ergebnis_label.config(text="Falsch!")
        for btn in self.antwort_buttons:
            btn.config(state="disabled")
        self.aktuelle_frage_index += 1
        if self.aktuelle_frage_index < len(self.fragen):
            self.root.after(1500, self.zeige_frage)
        else:
            self.frage_label.config(text=f"Quiz beendet! Punkte: {self.punkte}")
            self.ergebnis_label.config(text="")


if __name__ == "__main__":
    # fragen = [
    #     QuizFrage(
    #        "Wie heisst die Hauptstadt von Frankreich?",
    #        ["Berlin", "Paris", "Rom", "Madrid"],
    #        1,
    #    ),
    #    QuizFrage("Was ist 2+2?", ["3", "4", "5", "6"], 1),
    # ]

    rows = fetch_12_questions()  # Funktion fetch_12_questions aufrufen
    fragen = []  # leere liste für die Objekte der Klasse QuizFragen

    for (
        row
    ) in (
        rows
    ):  # rows ist eine Liste von tulpels mit Form (Fragetext, [Antwort A, Antwort B...], korrekterIndex)
        text = row[0]  # in text wird die Frage gespeichert
        answers = row[1]  # ""
        correct = row[2]  # ""

        q = QuizFrage(
            text, answers, correct
        )  # Es wird ein Objekt der Klasse Quizfrage erstellt

        fragen.append(q)  # Das Objekt wird in die Liste angehängt

    print(vars(fragen[0]))

    root = tk.Tk()
    root.title("Quizspiel")
    quiz = QuizGUI(root, fragen)
    root.mainloop()
