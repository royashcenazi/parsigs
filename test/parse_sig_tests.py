import unittest

from parsigs.parse_sig_api import StructuredSig, parse_sig


class ParseSigApiTest(unittest.TestCase):
    def test_parse_sig_basic(self):
        sig = "Take 1 tablet of aderol 3 times a day"
        expected = StructuredSig(drug="aderol", form="tablet", strength=None, frequencyType="Day", interval=3, singleDosageAmount=1.0, periodType=None, periodAmount=None)
        result = parse_sig(sig)
        self.assertEqual(result, expected)

    def test_parse_sig_strength(self):
        sig = "Take 1 tablet of ibuprofen 200mg 3 times a day"
        expected = StructuredSig(drug="ibuprofen", form="tablet", strength="200mg", frequencyType="Day", interval=3, singleDosageAmount=1.0, periodType=None, periodAmount=None)
        result = parse_sig(sig, "../research/example_model2/model-best")
        self.assertEqual(result, expected)

    def test_parse_sig_period(self):
        sig = "Take 2 capsules of amoxicillin 500mg every 12 days for 10 days"
        expected = StructuredSig(drug="amoxicillin", form="capsules", strength="500mg", frequencyType="Day", interval=12, singleDosageAmount=2.0, periodType="Day", periodAmount=10)
        result = parse_sig(sig)
        self.assertEqual(result, expected)

    def test_parse_sig_no_form(self):
        sig = "Take 1 Benadryl 3 times a day"
        expected = StructuredSig(drug="benadryl", form=None, strength=None, frequencyType="Day", interval=3, singleDosageAmount=1.0, periodType=None, periodAmount=None)
        result = parse_sig(sig)
        self.assertEqual(result, expected)

    def test_parse_sig_no_drug(self):
        sig = "Take two tablets 3 times a week"
        expected = StructuredSig(drug=None, form='tablets', strength=None, frequencyType="Week", interval=3, singleDosageAmount=2.0, periodType=None, periodAmount=None)
        result = parse_sig(sig)
        self.assertEqual(result, expected)


