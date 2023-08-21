import unittest

from parsigs.parse_sig_api import StructuredSig, SigParser


class TestParseSigApi(unittest.TestCase):
    sig_parser = SigParser()

    def test_parse_sig_basic(self):
        sig = "Take 1 tablet 3 times a day for 2 weeks"
        expected = StructuredSig(drug=None, form="tablet", strength=None, frequencyType="Day", interval=3, singleDosageAmount=1.0, periodType='Week', periodAmount=2, takeAsNeeded=False)
        result = self.sig_parser.parse(sig)[0]
        self.assertEqual(result, expected)

    def test_parse_sig_strength(self):
        sig = "Take 1 tablet of ibuprofen 200mg 3 times every day for 10 weeks"
        expected = StructuredSig(drug="ibuprofen", form="tablet", strength="200mg", frequencyType="Day", interval=3, singleDosageAmount=1.0, periodType="Week", periodAmount=10, takeAsNeeded=False)
        result = self.sig_parser.parse(sig)[0]
        self.assertEqual(result, expected)

    def test_parse_sig_period(self):
        sig = "Take 2 tabs of amoxicillin 500mg every 12 days for 10 days"
        expected = StructuredSig(drug="amoxicillin", form="tab", strength="500mg", frequencyType="Day", interval=12, singleDosageAmount=2.0, periodType="Day", periodAmount=10, takeAsNeeded=False)
        result = self.sig_parser.parse(sig)[0]
        self.assertEqual(result, expected)

    def test_parse_sig_period_year(self):
        sig = "Take 2 tabs of amoxicillin 500mg every 12 days for 2 years"
        expected = StructuredSig(drug="amoxicillin", form="tab", strength="500mg", frequencyType="Day", interval=12, 
                                 singleDosageAmount=2.0, periodType="Year", periodAmount=2, takeAsNeeded=False)
        result = self.sig_parser.parse(sig)[0]
        self.assertEqual(result, expected)

    def test_parse_no_drug(self):
        sig = "Take 1 pill 3 times a day"
        expected = StructuredSig(drug=None, form='pill', strength=None, frequencyType="Day", interval=3, singleDosageAmount=1.0, periodType=None, periodAmount=None, takeAsNeeded=False)
        result = self.sig_parser.parse(sig)[0]
        self.assertEqual(result, expected)

    def test_parse_sig_text_and_regular_numbers(self):
        sig = "Take two tablets of ibuprofen 3 times every week"
        expected = StructuredSig(drug='ibuprofen', form='tablet', strength=None, frequencyType="Week", interval=3, singleDosageAmount=2.0, periodType=None, periodAmount=None, takeAsNeeded=False)
        result = self.sig_parser.parse(sig)[0]
        self.assertEqual(result, expected)

    def test_unprocessed_sig(self):
        sig = "INHALE 2 puffs EVERY DAY"
        expected = StructuredSig(drug=None, form='puff', strength=None, frequencyType="Day", interval=1, singleDosageAmount=2.0, periodType=None, periodAmount=None, takeAsNeeded=False)
        result = self.sig_parser.parse(sig)[0]
        self.assertEqual(result, expected)

    def test_as_needed(self):
        sig = "TAKE 1 TABLET BY MOUTH EVERY 6 HOURS AS NEEDED FOR PAIN"
        expected = StructuredSig(drug=None, form='tablet', strength=None, frequencyType="Hour", interval=6, singleDosageAmount=1.0, periodType=None, periodAmount=None, takeAsNeeded=True)
        result = self.sig_parser.parse(sig)[0]
        self.assertEqual(result, expected)

    def test_parse_sig_short_form(self):
        sig = "Take 1 tab of Benadryl 3 times a day"
        expected = StructuredSig(drug='benadryl', form='tablet', strength=None, frequencyType="Day", interval=3, singleDosageAmount=1.0, periodType=None, periodAmount=None, takeAsNeeded=False)
        result = self.sig_parser.parse(sig)[0]
        self.assertEqual(result, expected)

    def test_parse_sig_no_form(self):
        sig = "Take 1 codeine 3 times a day"
        expected = StructuredSig(drug='codeine', form=None, strength=None, frequencyType="Day", interval=3, singleDosageAmount=1.0, periodType=None, periodAmount=None, takeAsNeeded=False)
        result = self.sig_parser.parse(sig)[0]
        self.assertEqual(result, expected)

    def test_parse_sig_every_other_time_unit(self):
        sig = "TAKE 1 TABLET BY MOUTH EVERY OTHER DAY"
        expected = StructuredSig(drug=None, form='tablet', strength=None, frequencyType="Day", interval=2, singleDosageAmount=1.0, periodType=None, periodAmount=None, takeAsNeeded=False)
        result = self.sig_parser.parse(sig)[0]
        self.assertEqual(result, expected)

    def test_parse_sig_latin(self):
        sig = "1 TAB of BENADRYL BID"
        expected = StructuredSig(drug="benadryl", form='tablet', strength=None, frequencyType="Day", interval=2, singleDosageAmount=1.0, periodType=None, periodAmount=None, takeAsNeeded=False)
        result = self.sig_parser.parse(sig)[0]
        self.assertEqual(result, expected)

    def test_parse_sig_capsules(self):
        sig = "Take 2 capsules of amoxicillin 500mg"
        expected = StructuredSig(drug="amoxicillin", form="capsule", strength="500mg", frequencyType=None, interval=None, singleDosageAmount=2.0, periodType=None, periodAmount=None, takeAsNeeded=False)
        result = self.sig_parser.parse(sig)[0]
        self.assertEqual(result, expected)

    def test_parse_multiple_instructions(self):
        sig = "take 1 tablet of atorvastatin every day and then 2 tablets every week"
        first_expected = StructuredSig(drug="atorvastatin", form="tablet", strength=None, frequencyType="Day",
                                       interval=1, singleDosageAmount=1.0, periodType=None, periodAmount=None,
                                       takeAsNeeded=False)
        second_expected = StructuredSig(drug="atorvastatin", form="tablet", strength=None, frequencyType="Week",
                                        interval=1, singleDosageAmount=2.0, periodType=None, periodAmount=None,
                                        takeAsNeeded=False)
        result = self.sig_parser.parse(sig)
        expected = [first_expected, second_expected]
        self.assertEqual(result, expected)

    def test_parse_multiple_instructions2(self):
        sig = "take two tablets of benadryl every two days and then 1 tablet as needed"
        first_expected = StructuredSig(drug="benadryl", form="tablet", strength=None, frequencyType="Day", interval=2,
                                       singleDosageAmount=2.0, periodType=None, periodAmount=None, takeAsNeeded=False)
        second_expected = StructuredSig(drug="benadryl", form="tablet", strength=None, frequencyType=None, interval=1,
                                        singleDosageAmount=1.0, periodType=None, periodAmount=None, takeAsNeeded=True)
        result = self.sig_parser.parse(sig)
        expected = [first_expected, second_expected]
        self.assertEqual(result, expected)

    def test_parse_multiple_instructions3(self):
        sig = "take two tablets of benadryl every two days and then 1 tablet every week for 1 month and than 1 tablet every month"
        first_expected = StructuredSig(drug="benadryl", form="tablet", strength=None, frequencyType="Day", interval=2,
                                       singleDosageAmount=2.0, periodType=None, periodAmount=None, takeAsNeeded=False)
        second_expected = StructuredSig(drug="benadryl", form="tablet", strength=None, frequencyType='Week', interval=1,
                                        singleDosageAmount=1.0, periodType='Month', periodAmount=1, takeAsNeeded=False)
        third_expected = StructuredSig(drug="benadryl", form="tablet", strength=None, frequencyType='Month', interval=1,
                                       singleDosageAmount=1.0, periodType=None, periodAmount=None, takeAsNeeded=False)
        result = self.sig_parser.parse(sig)
        expected = [first_expected, second_expected, third_expected]
        self.assertEqual(result, expected)

    def test_autocorrect_and__pre_process1(self):
        sig = "Tkae 1 tabet 3 tiems a day for 2 wekes"
        expected = StructuredSig(drug=None, form="tablet", strength=None, frequencyType="Day", interval=3,
                                 singleDosageAmount=1.0, periodType='Week', periodAmount=2, takeAsNeeded=False)
        result = self.sig_parser.parse(sig)[0]
        self.assertEqual(result, expected)

    def test_autocorrect_and__pre_process2(self):
        sig = "Tkae 1 talbet of ibuprofen 200mg 3 tiems every day for 10 wekes"
        expected = StructuredSig(drug="ibuprofen", form="tablet", strength="200mg", frequencyType="Day", interval=3,
                                 singleDosageAmount=1.0, periodType="Week", periodAmount=10, takeAsNeeded=False)
        result = self.sig_parser.parse(sig)[0]
        self.assertEqual(result, expected)

    # TODO fix and find a way to give certain words priority in autocorrect
    # def test_autocorrect_and__pre_process3(self):
    #     sig = "Take 1 TableT of (Bendaryl) 3 times a day"
    #     expected = StructuredSig(drug='benadryl', form='tablet', strength=None, frequencyType="Day", interval=3, singleDosageAmount=1.0, periodType=None, periodAmount=None, takeAsNeeded=False)
    #     result = self.sig_parser.parse(sig)[0]
    #     self.assertEqual(result, expected)
    #
    def test_autocorrect_and__pre_process4(self):
        sig = "Atke 1 tab of Benadryl 3 tmies a day"
        expected = StructuredSig(drug='benadryl', form='tablet', strength=None, frequencyType="Day", interval=3,
                                 singleDosageAmount=1.0, periodType=None, periodAmount=None, takeAsNeeded=False)
        result = self.sig_parser.parse(sig)[0]
        self.assertEqual(result, expected)

    def test_autocorrect_and_pre_process5(self):
        sig = "takr 1 tablet of Benadryl 3 times a dya"
        expected = StructuredSig(drug='benadryl', form='tablet', strength=None, frequencyType="Day", interval=3,
                                 singleDosageAmount=1.0, periodType=None, periodAmount=None, takeAsNeeded=False)
        result = self.sig_parser.parse(sig)[0]
        self.assertEqual(result, expected)

    # def test_autocorrect_and_pre_process6(self):
    #     sig = "tkae 1 talbet of atorva$tatin every day and hten 2 talbets every week"
    #     first_expected = StructuredSig(drug="atorvastatin", form="tablet", strength=None, frequencyType="Day", interval=1, singleDosageAmount=1.0, periodType=None, periodAmount=None, takeAsNeeded=False)
    #     second_expected = StructuredSig(drug="atorvastatin", form="tablets", strength=None, frequencyType="Week", interval=1, singleDosageAmount=2.0, periodType=None, periodAmount=None, takeAsNeeded=False)
    #     result = self.sig_parser.parse(sig)
    #     expected = [first_expected, second_expected]
    #     self.assertEqual(result, expected)

    def test_autocorrect_and_pre_process7(self):
        sig = "tkae two talbets of benadryl every two days and then 1 talbet every week for 1 month and than 1 talbet every month"
        first_expected = StructuredSig(drug="benadryl", form="tablet", strength=None, frequencyType="Day", interval=2,
                                       singleDosageAmount=2.0, periodType=None, periodAmount=None, takeAsNeeded=False)
        second_expected = StructuredSig(drug="benadryl", form="tablet", strength=None, frequencyType='Week', interval=1,
                                        singleDosageAmount=1.0, periodType='Month', periodAmount=1, takeAsNeeded=False)
        third_expected = StructuredSig(drug="benadryl", form="tablet", strength=None, frequencyType='Month', interval=1,
                                       singleDosageAmount=1.0, periodType=None, periodAmount=None, takeAsNeeded=False)
        result = self.sig_parser.parse(sig)
        expected = [first_expected, second_expected, third_expected]
        self.assertEqual(result, expected)