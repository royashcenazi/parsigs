import unittest
from krovetzstemmer import Stemmer

class TestStemmer(unittest.TestCase):
    def test_stemmer(self):
        stemmer = Stemmer()
        self.assertEqual(stemmer.stem("tablets"), "tablet")
        self.assertEqual(stemmer.stem("puffs"), "puff")
        self.assertEqual(stemmer.stem("parties"), "party")
        self.assertEqual(stemmer.stem("capsules"), "capsule")
        self.assertEqual(stemmer.stem("drops"), "drop")
        self.assertEqual(stemmer.stem("layers"), "layer")
        self.assertEqual(stemmer.stem("sprays"), "spray")