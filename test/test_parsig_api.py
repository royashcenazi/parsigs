import unittest

from parsigs.parse_sig_api import StructuredSig, parse_sig


class TestParseSigApi(unittest.TestCase):
    def test_parse_sig_basic(self):
        sig = "Take 1 tablet 3 times a day for 2 weeks"
        expected = StructuredSig(drug=None, form="tablet", strength=None, frequencyType="Day", interval=3, singleDosageAmount=1.0, periodType='Week', periodAmount=2)
        result = parse_sig(sig)
        self.assertEqual(result, expected)

    def test_parse_sig_strength(self):
        sig = "Take 1 tablet of ibuprofen 200mg 3 times every day"
        expected = StructuredSig(drug="ibuprofen", form="tablet", strength="200mg", frequencyType="Day", interval=3, singleDosageAmount=1.0, periodType=None, periodAmount=None)
        result = parse_sig(sig)
        self.assertEqual(result, expected)

    def test_parse_sig_period(self):
        sig = "Take 2 tabs of amoxicillin 500mg every 12 days for 10 days"
        expected = StructuredSig(drug="amoxicillin", form="tabs", strength="500mg", frequencyType="Day", interval=12, singleDosageAmount=2.0, periodType="Day", periodAmount=10)
        result = parse_sig(sig)
        self.assertEqual(result, expected)

    def test_parse_no_drug(self):
        sig = "Take 1 pill 3 times a day"
        expected = StructuredSig(drug=None, form='pill', strength=None, frequencyType="Day", interval=3, singleDosageAmount=1.0, periodType=None, periodAmount=None)
        result = parse_sig(sig)
        self.assertEqual(result, expected)

    def test_parse_sig_text_and_regular_numbers(self):
        sig = "Take two tablets of ibuprofen 3 times every week"
        expected = StructuredSig(drug='ibuprofen', form='tablets', strength=None, frequencyType="Week", interval=3, singleDosageAmount=2.0, periodType=None, periodAmount=None)
        result = parse_sig(sig)
        self.assertEqual(result, expected)

    def test_unprocessed_sig(self):
        sig = "INHALE 2 puffs EVERY DAY"
        expected = StructuredSig(drug=None, form='puffs', strength=None, frequencyType="Day", interval=1, singleDosageAmount=2.0, periodType=None, periodAmount=None)
        result = parse_sig(sig)
        self.assertEqual(result, expected)

    # def test_parse_sig_no_form(self):
    #     sig = "Take 1 Benadryl 3 times a day"
    #     expected = StructuredSig(drug=None, form='pill', strength=None, frequencyType="Day", interval=3, singleDosageAmount=1.0, periodType=None, periodAmount=None)
    #     result = parse_sig(sig)
    #     self.assertEqual(result, expected)

    # def test_parse_sig_period(self):
    #     sig = "Take 2 capsules of amoxicillin 500mg"
    #     expected = StructuredSig(drug="amoxicillin", form="capsules", strength="500mg", frequencyType="Day", interval=12, singleDosageAmount=2.0, periodType="Day", periodAmount=10)
    #     result = parse_sig(sig)
    #     self.assertEqual(result, expected)
