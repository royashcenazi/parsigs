import unittest

from parsigs.parse_sig_api import StructuredSig, SigParser


class TestParseSigApi(unittest.TestCase):
    sig_parser = SigParser()

    def test_parse_sig_basic(self):
        sig = "Take 1 tablet 3 times a day for 2 weeks"
        expected = StructuredSig(drug=None, form="tablet", strength=None, frequencyType="Day", interval=3, singleDosageAmount=1.0, periodType='Week', periodAmount=2, takeAsNeeded=False)
        result = self.sig_parser.parse(sig)
        self.assertEqual(result, expected)

    def test_parse_sig_strength(self):
        sig = "Take 1 tablet of ibuprofen 200mg 3 times every day"
        expected = StructuredSig(drug="ibuprofen", form="tablet", strength="200mg", frequencyType="Day", interval=3, singleDosageAmount=1.0, periodType=None, periodAmount=None, takeAsNeeded=False)
        result = self.sig_parser.parse(sig)
        self.assertEqual(result, expected)

    def test_parse_sig_period(self):
        sig = "Take 2 tabs of amoxicillin 500mg every 12 days for 10 days"
        expected = StructuredSig(drug="amoxicillin", form="tabs", strength="500mg", frequencyType="Day", interval=12, singleDosageAmount=2.0, periodType="Day", periodAmount=10, takeAsNeeded=False)
        result = self.sig_parser.parse(sig)
        self.assertEqual(result, expected)

    def test_parse_no_drug(self):
        sig = "Take 1 pill 3 times a day"
        expected = StructuredSig(drug=None, form='pill', strength=None, frequencyType="Day", interval=3, singleDosageAmount=1.0, periodType=None, periodAmount=None, takeAsNeeded=False)
        result = self.sig_parser.parse(sig)
        self.assertEqual(result, expected)

    def test_parse_sig_text_and_regular_numbers(self):
        sig = "Take two tablets of ibuprofen 3 times every week"
        expected = StructuredSig(drug='ibuprofen', form='tablets', strength=None, frequencyType="Week", interval=3, singleDosageAmount=2.0, periodType=None, periodAmount=None, takeAsNeeded=False)
        result = self.sig_parser.parse(sig)
        self.assertEqual(result, expected)

    def test_unprocessed_sig(self):
        sig = "INHALE 2 puffs EVERY DAY"
        expected = StructuredSig(drug=None, form='puffs', strength=None, frequencyType="Day", interval=1, singleDosageAmount=2.0, periodType=None, periodAmount=None, takeAsNeeded=False)
        result = self.sig_parser.parse(sig)
        self.assertEqual(result, expected)

    def test_as_needed(self):
        sig = "TAKE 1 TABLET BY MOUTH EVERY 6 HOURS AS NEEDED FOR PAIN"
        expected = StructuredSig(drug=None, form='tablet', strength=None, frequencyType="Hour", interval=6, singleDosageAmount=1.0, periodType=None, periodAmount=None, takeAsNeeded=True)
        result = self.sig_parser.parse(sig)
        self.assertEqual(result, expected)

    def test_parse_sig_short_form(self):
        sig = "Take 1 tab of Benadryl 3 times a day"
        expected = StructuredSig(drug='benadryl', form='tablet', strength=None, frequencyType="Day", interval=3, singleDosageAmount=1.0, periodType=None, periodAmount=None, takeAsNeeded=False)
        result = self.sig_parser.parse(sig)
        self.assertEqual(result, expected)

    def test_parse_sig_no_form(self):
        sig = "Take 1 codaine 3 times a day"
        expected = StructuredSig(drug='codaine', form=None, strength=None, frequencyType="Day", interval=3, singleDosageAmount=1.0, periodType=None, periodAmount=None, takeAsNeeded=False)
        result = self.sig_parser.parse(sig)
        self.assertEqual(result, expected)

    def test_parse_sig_every_other_time_unit(self):
        sig = "TAKE 1 TABLET BY MOUTH EVERY OTHER DAY"
        expected = StructuredSig(drug=None, form='tablet', strength=None, frequencyType="Day", interval=2, singleDosageAmount=1.0, periodType=None, periodAmount=None, takeAsNeeded=False)
        result = self.sig_parser.parse(sig)
        self.assertEqual(result, expected)

    def test_parse_sig_latin(self):
        sig = "1 TAB of BENADRYL BID"
        expected = StructuredSig(drug="benadryl", form='tablet', strength=None, frequencyType="Day", interval=2, singleDosageAmount=1.0, periodType=None, periodAmount=None, takeAsNeeded=False)
        result = self.sig_parser.parse(sig)
        self.assertEqual(result, expected)

    # def test_parse_sig_capsules(self):
    #     sig = "Take 2 capsules of amoxicillin 500mg"
    #     expected = StructuredSig(drug="amoxicillin", form="capsules", strength="500mg", frequencyType=None, interval=None, singleDosageAmount=2.0, periodType=None, periodAmount=None, take_as_needed=False)
    #     result = parse_sig(sig)
    #     self.assertEqual(result, expected)
