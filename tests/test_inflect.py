import unittest
import inflect


class TestInflect(unittest.TestCase):
    def test_inflect(self):
        self.assertEqual(inflect.engine().singular_noun("tablets"), "tablet")
        self.assertEqual(inflect.engine().singular_noun("puffs"), "puff")
        self.assertEqual(inflect.engine().singular_noun("parties"), "party")
        self.assertEqual(inflect.engine().singular_noun("capsules"), "capsule")
        self.assertEqual(inflect.engine().singular_noun("drops"), "drop")
        self.assertEqual(inflect.engine().singular_noun("layers"), "layer")
        self.assertEqual(inflect.engine().singular_noun("sprays"), "spray")
