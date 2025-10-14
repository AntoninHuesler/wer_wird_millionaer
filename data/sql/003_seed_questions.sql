-- ===== 8 leichte Fragen =====
INSERT INTO questions(text,answer_a,answer_b,answer_c,answer_d,correct_index,difficulty) VALUES
('Hauptstadt der Schweiz?','Zürich','Bern','Basel','Luzern',1,'leicht'),
('2 + 2 = ?','3','4','5','6',1,'leicht'),
('Wie viele Kontinente gibt es?','5','6','7','8',2,'leicht'),
('Welche Farbe hat eine reife Banane?','Grün','Gelb','Rot','Blau',1,'leicht'),
('Welches Tier bellt?','Katze','Hund','Kuh','Pferd',1,'leicht'),
('Wer erfand den Buchdruck mit beweglichen Lettern?','Johannes Gutenberg','Leonardo da Vinci','Isaac Newton','Albert Einstein',0,'leicht'),
('Wie viele Minuten hat eine Stunde?','30','45','60','90',2,'leicht'),
('Welcher Wochentag folgt auf Montag?','Sonntag','Dienstag','Mittwoch','Donnerstag',1,'leicht');

-- ===== 8 mittlere Fragen =====
INSERT INTO questions(text,answer_a,answer_b,answer_c,answer_d,correct_index,difficulty) VALUES
('Wer schrieb "Faust"?','Friedrich Schiller','Johann Wolfgang von Goethe','Gotthold Ephraim Lessing','Heinrich Heine',1,'mittel'),
('Welcher Planet ist der vierte von der Sonne?','Venus','Mars','Jupiter','Saturn',1,'mittel'),
('Chemisches Symbol für Gold?','Au','Ag','Fe','Cu',0,'mittel'),
('Hauptstadt von Kanada?','Toronto','Ottawa','Montreal','Vancouver',1,'mittel'),
('Welcher Fluss fliesst durch Wien?','Rhein','Donau','Elbe','Po',1,'mittel'),
('Wer malte die "Mona Lisa"?','Michelangelo','Rembrandt','Pablo Picasso','Leonardo da Vinci',3,'mittel'),
('Wie viele Spieler hat ein Fussballteam auf dem Feld?','9','10','11','12',2,'mittel'),
('Grösstes Organ des menschlichen Körpers?','Haut','Leber','Lunge','Herz',0,'mittel');

-- ===== 8 schwere Fragen =====
INSERT INTO questions(text,answer_a,answer_b,answer_c,answer_d,correct_index,difficulty) VALUES
('In welchem Jahr begann der Erste Weltkrieg?','1912','1914','1916','1918',1,'schwer'),
('Kleinste Primzahl?','1','2','3','4',1,'schwer'),
('Wer komponierte die Oper "Die Zauberflöte"?','Joseph Haydn','Ludwig van Beethoven','Wolfgang Amadeus Mozart','Richard Wagner',2,'schwer'),
('Welches Element hat die höchste elektrische Leitfähigkeit?','Kupfer','Silber','Gold','Aluminium',1,'schwer'),
('Hauptstadt von Australien?','Sydney','Melbourne','Canberra','Perth',2,'schwer'),
('Welche Sprache hat die meisten Muttersprachler weltweit?','Englisch','Mandarin-Chinesisch','Spanisch','Hindi',1,'schwer'),
('Welches Land hat die längste Küstenlinie?','Kanada','Russland','Indonesien','Australien',0,'schwer'),
('Höchster Berg Afrikas?','Mount Kenia','Ruwenzori','Kilimandscharo','Atlas',2,'schwer');
