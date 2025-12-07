import unittest
import repo_question


class TestRepoQuestion(unittest.TestCase):

    def test_pick_returns_list(self):
        """pick sollte eine Liste zurückgeben"""
        result = repo_question.pick("leicht", 2)
        self.assertIsInstance(result, list)

    def test_pick_elements_structure(self):
        """Jedes Element sollte ein Tupel (Fragetext, [Antworten], korrekterIndex) sein"""
        result = repo_question.pick("leicht", 1)
        if result:  # nur prüfen, wenn DB nicht leer
            question = result[0]
            # Tupel mit 3 Elementen
            self.assertIsInstance(question, tuple)
            self.assertEqual(len(question), 3)
            # Fragetext ist String
            self.assertIsInstance(question[0], str)
            # Antworten ist Liste mit 4 Strings
            self.assertIsInstance(question[1], list)
            self.assertEqual(len(question[1]), 4)
            for ans in question[1]:
                self.assertIsInstance(ans, str)
            # korrekterIndex ist int
            self.assertIsInstance(question[2], int)

    def test_fetch_12_questions_length(self):
        """fetch_12_questions sollte genau 12 Fragen liefern"""
        result = repo_question.fetch_12_questions()
        self.assertEqual(len(result), 12)


if __name__ == "__main__":
    unittest.main()
