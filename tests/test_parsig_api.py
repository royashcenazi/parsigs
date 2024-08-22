import unittest

from parsigs.parse_sig_api import StructuredSig, SigParser


class TestParseSigApi(unittest.TestCase):
    sig_parser = SigParser()

    def test_parse_sig_basic(self):
        sig = "Take 1 tablet 3 times a day for 2 weeks"
        expected = StructuredSig(drug=None, form="tablet", strength=None, frequencyType="Day", interval=1, times=3, singleDosageAmount=1.0, periodType='Week', periodAmount=2, takeAsNeeded=False)
        result = self.sig_parser.parse(sig)[0]
        self.assertEqual(result, expected)

    # When there is a mix of times and every, the model does not tag well the frequency
    # Not sure if this is a valid use case (instead of times probably it would be "take 3 tablets every 2 days" but in order
    # To solve, designated training examples should be introduced to the model
    # def test_parse_sig_interval_and_times(self):
    #     sig = "Take 1 tablet of ibuprofen 200mg 3 times every 2 weeks for 10 weeks"
    #     expected = StructuredSig(drug="ibuprofen", form="tablet", strength="200mg", frequencyType="Day", times=3, interval=2, singleDosageAmount=1.0, periodType="Week", periodAmount=10, takeAsNeeded=False)
    #     result = self.sig_parser.parse(sig)[0]
    #     self.assertEqual(result, expected)

    # def test_parse_sig_strength(self):
    #     sig = "Take 1 tablet of ibuprofen 200mg 3 times every two days for 10 weeks"
    #     expected = StructuredSig(drug="ibuprofen", form="tablet", strength="200mg", frequencyType="Day", interval=3, singleDosageAmount=1.0, periodType="Week", periodAmount=10, takeAsNeeded=False)
    #     result = self.sig_parser.parse(sig)[0]
    #     self.assertEqual(result, expected)
    def test_parse_sig_period(self):
        sig = "Take 2 tabs of amoxicillin 500mg every 12 days for 10 days"
        expected = StructuredSig(drug="amoxicillin", form="tablet", strength="500mg", times=None, frequencyType="Day", interval=12, singleDosageAmount=2.0, periodType="Day", periodAmount=10, takeAsNeeded=False)
        result = self.sig_parser.parse(sig)[0]
        self.assertEqual(result, expected)

    def test_parse_sig_period_year(self):
        sig = "Take 2 tabs of amoxicillin 500mg every 12 days for 2 years"
        expected = StructuredSig(drug="amoxicillin", form="tablet", strength="500mg", frequencyType="Day", interval=12,
                                 singleDosageAmount=2.0, periodType="Year", periodAmount=2, takeAsNeeded=False, times=None)
        result = self.sig_parser.parse(sig)[0]
        self.assertEqual(result, expected)

    def test_parse_no_drug(self):
        sig = "Take 1 pill 3 times a day"
        expected = StructuredSig(drug=None, form='pill', strength=None, frequencyType="Day", interval=1, times=3, singleDosageAmount=1.0, periodType=None, periodAmount=None, takeAsNeeded=False)
        result = self.sig_parser.parse(sig)[0]
        self.assertEqual(result, expected)

    def test_parse_sig_text_and_regular_numbers(self):
        sig = "Take two tablets of ibuprofen 3 times every week"
        expected = StructuredSig(drug='ibuprofen', form='tablet', strength=None, frequencyType="Week", interval=1, times=3, singleDosageAmount=2.0, periodType=None, periodAmount=None, takeAsNeeded=False)
        result = self.sig_parser.parse(sig)[0]
        self.assertEqual(result, expected)

    def test_unprocessed_sig(self):
        sig = "INHALE 2 puffs EVERY DAY"
        expected = StructuredSig(drug=None, form='puff', strength=None, frequencyType="Day", interval=1, times=None, singleDosageAmount=2.0, periodType=None, periodAmount=None, takeAsNeeded=False)
        result = self.sig_parser.parse(sig)[0]
        self.assertEqual(result, expected)

    def test_as_needed(self):
        sig = "TAKE 1 TABLET BY MOUTH EVERY 6 HOURS AS NEEDED FOR PAIN"
        expected = StructuredSig(drug=None, form='tablet', strength=None, frequencyType="Hour", interval=6, times=None, singleDosageAmount=1.0, periodType=None, periodAmount=None, takeAsNeeded=True)
        result = self.sig_parser.parse(sig)[0]
        self.assertEqual(result, expected)

    def test_parse_sig_short_form(self):
        sig = "Take 1 tab of Benadryl 3 times a day"
        expected = StructuredSig(drug='benadryl', form='tablet', strength=None, frequencyType="Day", interval=1, times=3, singleDosageAmount=1.0, periodType=None, periodAmount=None, takeAsNeeded=False)
        result = self.sig_parser.parse(sig)[0]
        self.assertEqual(result, expected)

    def test_parse_sig_no_form(self):
        sig = "Take 1 codeine 3 times a day"
        expected = StructuredSig(drug='codeine', form=None, strength=None, frequencyType="Day", times=3, interval=1, singleDosageAmount=1.0, periodType=None, periodAmount=None, takeAsNeeded=False)
        result = self.sig_parser.parse(sig)[0]
        self.assertEqual(result, expected)

    def test_parse_sig_every_other_time_unit(self):
        sig = "TAKE 1 TABLET BY MOUTH EVERY OTHER DAY"
        expected = StructuredSig(drug=None, form='tablet', strength=None, frequencyType="Day", interval=2, times=None, singleDosageAmount=1.0, periodType=None, periodAmount=None, takeAsNeeded=False)
        result = self.sig_parser.parse(sig)[0]
        self.assertEqual(result, expected)

    def test_parse_sig_latin(self):
        sig = "1 TAB of BENADRYL BID"
        expected = StructuredSig(drug="benadryl", form='tablet', strength=None, interval=1, frequencyType="Day", times=2, singleDosageAmount=1.0, periodType=None, periodAmount=None, takeAsNeeded=False)
        result = self.sig_parser.parse(sig)[0]
        self.assertEqual(result, expected)

    def test_parse_sig_latin2(self):
        sig = "1 TAB of BENADRYL qd times"
        expected = StructuredSig(drug="benadryl", form='tablet', strength=None, interval=1, frequencyType="Day", times=1, singleDosageAmount=1.0, periodType=None, periodAmount=None, takeAsNeeded=False)
        result = self.sig_parser.parse(sig)[0]
        self.assertEqual(result, expected)

    def test_parse_sig_latin3(self):  # test the latin hour abbreviation q_h (take every _ hours)
        sig = "1 TAB of BENADRYL q7h times for 2 weeks"
        expected = StructuredSig(drug="benadryl", form='tablet', strength=None, interval=7, frequencyType="Hour",
                                 times=1, singleDosageAmount=1.0, periodType="Week", periodAmount=2, takeAsNeeded=False)
        result = self.sig_parser.parse(sig)[0]
        self.assertEqual(result, expected)

    def test_parse_sig_latin_with_period(self):
        sig = "take 4 TABS q.4.d for 4 weeks"
        expected = StructuredSig(drug=None, form='tablet', strength=None, interval=4, frequencyType="Day", times=1,
                                 singleDosageAmount=4.0, periodType="Week", periodAmount=4, takeAsNeeded=False)
        result = self.sig_parser.parse(sig)[0]
        self.assertEqual(result, expected)

    def test_parse_sig_latin_end_of_sentence(self):
        sig = "Take 3 capsules by mouth q12h"
        expected = StructuredSig(drug=None, form='capsule', strength=None, interval=12, frequencyType="Hour", times=1, singleDosageAmount=3.0, periodType=None, periodAmount=None, takeAsNeeded=False)
        result = self.sig_parser.parse(sig)[0]
        self.assertEqual(result, expected)

    def test_parse_sig_latin_every_other_day(self):
        sig = "Take 4 tabs by mouth Q.O.D for 2 weeks"
        expected = StructuredSig(drug=None, form='tablet', strength=None, interval=2, frequencyType="Day", times=1, singleDosageAmount=4.0, periodType="Week", periodAmount=2, takeAsNeeded=False)
        result = self.sig_parser.parse(sig)[0]
        self.assertEqual(result, expected)

    def test_parse_sig_latin_capital(self):
        sig = "Take 1 tab by mouth Q6D for 8 weeks"
        expected = StructuredSig(drug=None, form='tablet', strength=None, interval=6, frequencyType="Day", times=1,
                                 singleDosageAmount=1.0, periodType="Week", periodAmount=8, takeAsNeeded=False)
        result = self.sig_parser.parse(sig)[0]
        self.assertEqual(result, expected)

    def test_parse_sig_latin_tid(self):
        sig = "1 tab of amoxicillin T.I.D for 1 month"
        expected = StructuredSig(drug="amoxicillin", form='tablet', strength=None, interval=1, frequencyType="Day", times=3,
                                 singleDosageAmount=1.0, periodType="Month", periodAmount=1, takeAsNeeded=False)
        result = self.sig_parser.parse(sig)[0]
        self.assertEqual(result, expected)

    def test_parse_sig_latin_weekly(self):
        sig = "inhale 3 puffs of Albuterol Q.I.W as needed"
        expected = StructuredSig(drug="albuterol", form='puff', strength=None, interval=1, frequencyType="Week", times=4,
                                 singleDosageAmount=3.0, periodType=None, periodAmount=None, takeAsNeeded=True)
        result = self.sig_parser.parse(sig)[0]
        self.assertEqual(result, expected)

    def test_parse_sig_capsules(self):
        sig = "Take 2 capsules of amoxicillin 500mg"
        expected = StructuredSig(drug="amoxicillin", form="capsule", strength="500mg", frequencyType=None, interval=1, times=None, singleDosageAmount=2.0, periodType=None, periodAmount=None, takeAsNeeded=False)
        result = self.sig_parser.parse(sig)[0]
        self.assertEqual(result, expected)

    def test_parse_sig_capsules2(self):
        sig = "Take 1 capsule by mouth twice daily (every 12 hours)"
        expected = StructuredSig(drug=None, form="capsule", strength=None, frequencyType="Day", interval=1, times=2, singleDosageAmount=1.0, periodType=None, periodAmount=None, takeAsNeeded=False)
        result = self.sig_parser.parse(sig)[0]
        self.assertEqual(result, expected)


    def test_parse_multiple_instructions(self):
        sig = "take 1 tablet of atorvastatin every day and then 2 tablets every week"
        first_expected = StructuredSig(drug="atorvastatin", form="tablet", strength=None, frequencyType="Day",
                                       interval=1, singleDosageAmount=1.0, times=None, periodType=None, periodAmount=None,
                                       takeAsNeeded=False)
        second_expected = StructuredSig(drug="atorvastatin", form="tablet", strength=None, frequencyType="Week",
                                        interval=1, singleDosageAmount=2.0, times=None, periodType=None, periodAmount=None,
                                        takeAsNeeded=False)
        result = self.sig_parser.parse(sig)
        expected = [first_expected, second_expected]
        self.assertEqual(result, expected)

    def test_parse_multiple_instructions2(self):
        sig = "take two tablets of benadryl every two days and then 1 tablet as needed"
        first_expected = StructuredSig(drug="benadryl", form="tablet", strength=None, frequencyType="Day", interval=2,
                                       singleDosageAmount=2.0, periodType=None, times=None, periodAmount=None, takeAsNeeded=False)
        second_expected = StructuredSig(drug="benadryl", form="tablet", strength=None, frequencyType=None, interval=1,
                                        singleDosageAmount=1.0, periodType=None, times=None, periodAmount=None, takeAsNeeded=True)
        result = self.sig_parser.parse(sig)
        expected = [first_expected, second_expected]
        self.assertEqual(result, expected)

    def test_parse_multiple_instructions3(self):
        sig = "take two tablets of benadryl every two days and then 1 tablet every week for 1 month and than 1 tablet every month"
        first_expected = StructuredSig(drug="benadryl", form="tablet", strength=None, frequencyType="Day", interval=2,
                                       singleDosageAmount=2.0, periodType=None, times=None, periodAmount=None, takeAsNeeded=False)
        second_expected = StructuredSig(drug="benadryl", form="tablet", strength=None, times=None, frequencyType='Week', interval=1,
                                        singleDosageAmount=1.0, periodType='Month', periodAmount=1, takeAsNeeded=False)
        third_expected = StructuredSig(drug="benadryl", form="tablet", strength=None, frequencyType='Month', interval=1,
                                       singleDosageAmount=1.0, periodType=None, times=None, periodAmount=None, takeAsNeeded=False)
        result = self.sig_parser.parse(sig)
        expected = [first_expected, second_expected, third_expected]
        self.assertEqual(result, expected)

    def test_autocorrect_and__pre_process1(self):
        sig = "Tkae 1 tabet 3 tiems a day for 2 wekes"
        expected = StructuredSig(drug=None, form="tablet", strength=None, frequencyType="Day", interval=1, times=3,
                                 singleDosageAmount=1.0, periodType='Week', periodAmount=2, takeAsNeeded=False)
        result = self.sig_parser.parse(sig)[0]
        self.assertEqual(result, expected)

    def test_autocorrect_and__pre_process2(self):
        sig = "Tkae 1 talbet of ibuprofen 200mg 3 tiems every day for 10 wekes"
        expected = StructuredSig(drug="ibuprofen", form="tablet", strength="200mg", frequencyType="Day", interval=1, times=3,
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
        expected = StructuredSig(drug='benadryl', form='tablet', strength=None, frequencyType="Day", interval=1, times=3,
                                 singleDosageAmount=1.0, periodType=None, periodAmount=None, takeAsNeeded=False)
        result = self.sig_parser.parse(sig)[0]
        self.assertEqual(result, expected)

    def test_autocorrect_and_pre_process5(self):
        sig = "takr 1 tablet of Benadryl 3 times a dya"
        expected = StructuredSig(drug='benadryl', form='tablet', strength=None, frequencyType="Day", interval=1, times=3,
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
        first_expected = StructuredSig(drug="benadryl", form="tablet", strength=None, frequencyType="Day", interval=2, times=None,
                                       singleDosageAmount=2.0, periodType=None, periodAmount=None, takeAsNeeded=False)
        second_expected = StructuredSig(drug="benadryl", form="tablet", strength=None, frequencyType='Week', interval=1, times=None,
                                        singleDosageAmount=1.0, periodType='Month', periodAmount=1, takeAsNeeded=False)
        third_expected = StructuredSig(drug="benadryl", form="tablet", strength=None, frequencyType='Month', interval=1, times=None,
                                       singleDosageAmount=1.0, periodType=None, periodAmount=None, takeAsNeeded=False)
        result = self.sig_parser.parse(sig)
        expected = [first_expected, second_expected, third_expected]
        self.assertEqual(result, expected)
