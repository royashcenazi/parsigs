import unittest

from parsigs.parse_sig_api import StructuredSig, parse_sig


class ParseSigApiTest(unittest.TestCase):
    def test_parse_sig_basic(self):
        sig = "Take 1 tablet of ibuprofen 3 times a day"
        expected = StructuredSig(drug="ibuprofen", form="tablet", strength=None, frequencyType="Day", interval=3, singleDosageAmount=1, periodType=None, periodAmount=None)
        result = parse_sig(sig)
        self.assertEqual(result, expected)

    def test_parse_sig_strength(self):
        sig = "Take 1 tablet of ibuprofen 200mg 3 times a day"
        expected = StructuredSig(drug="ibuprofen", form="tablet", strength="200mg", frequencyType="Day", interval=3, singleDosageAmount='1', periodType=None, periodAmount=None)
        result = parse_sig(sig, "../research/example_model2/model-best")
        self.assertEqual(result, expected)

    def test_parse_sig_period(self):
        sig = "Take 2 capsules of amoxicillin 500mg every 12 hours for 10 days"
        expected = StructuredSig(drug="amoxicillin", form="capsules", strength="500mg", frequencyType="every", interval=12, singleDosageAmount=2, periodType="days", periodAmount=10)
        result = parse_sig(sig)
        self.assertEqual(result, expected)

    def test_parse_sig_no_form(self):
        sig = "Take 1 ibuprofen 3 times a day"
        expected = StructuredSig(drug="ibuprofen", form="", strength="", frequencyType="times a day", interval=3, singleDosageAmount=1, periodType="", periodAmount=0)
        result = parse_sig(sig)
        self.assertEqual(result, expected)


