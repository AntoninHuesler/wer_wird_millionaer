CREATE TABLE IF NOT EXISTS questions ( -- legt die tabelle "questions" an wenn sie nicht existiert
    id INTEGER PRIMARY KEY, -- Spalte "id" als Primärschlüssel (fortlaufend nummerier)
    text TEXT NOT NULL, -- Spalte "text" enthält die Frage als text (Pflichtfeld)
    answer_a TEXT NOT NULL, -- Antwort A (Pflichtfeld).
    answer_b TEXT NOT NULL, -- Antwort B (Pflichtfeld).
    answer_c TEXT NOT NULL, -- Antwort C (Pflichtfeld).
    answer_d TEXT NOT NULL, -- Antwort D (Pflichtfeld).
    correct_index INTEGER NOT NULL  -- Index der richtigen Antwort (0..3),
        CHECK (correct_index BETWEEN 0 AND 3),  -- "correct_index" muss zwischen 0-3 sein
    difficulty TEXT NOT NULL  -- Schwierigkeitsgrad der Frage (Pflichtfeld),
        CHECK (difficulty IN ('leicht','mittel','schwer'))  --nur diese drei Strings sind erlaubt.
); 