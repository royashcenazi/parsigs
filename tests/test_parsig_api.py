import unittest

from parsigs.parse_sig_api import StructuredSig, SigParser


class TestParseSigApi(unittest.TestCase):
    sig_parser = SigParser()

    def test_parse_sig_basic(self):
        sig = "Take 1 tablet 3 times a day for 2 weeks"
        expected = StructuredSig(drug=None, form="tablet", strength=None, frequencyType="Day", interval=3, 
                                 singleDosageAmount=1.0, periodType='Week', periodAmount=2, takeAsNeeded=False)
        result = self.sig_parser.parse(sig)[0]
        self.assertEqual(result, expected)
    
    # we get None instead of 1.0 in dosageAmount
    # def test_parse_sig_with_a_instead_of_1(self):
    #     sig = "Take a tablet of amoxicillin 500mg every day"
    #     expected = StructuredSig(drug="amoxicillin", form="tablet", strength="500mg", frequencyType="Day", interval=1, 
    #                              singleDosageAmount=1.0, periodType=None, periodAmount=None, takeAsNeeded=False)
    #     result = self.sig_parser.parse(sig)[0]
    #     self.assertEqual(result, expected)

    def test_parse_sig_strength(self):
        sig = "Take 1 tablet of ibuprofen 200mg 3 times every day for 10 weeks"
        expected = StructuredSig(drug="ibuprofen", form="tablet", strength="200mg", frequencyType="Day", interval=3, 
                                 singleDosageAmount=1.0, periodType="Week", periodAmount=10, takeAsNeeded=False)
        result = self.sig_parser.parse(sig)[0]
        self.assertEqual(result, expected)
    
    def test_parse_sig_period(self):
        sig = "Take 2 tabs of amoxicillin 500mg every 12 days for 10 days"
        expected = StructuredSig(drug="amoxicillin", form="tab", strength="500mg", frequencyType="Day", interval=12, 
                                 singleDosageAmount=2.0, periodType="Day", periodAmount=10, takeAsNeeded=False)
        result = self.sig_parser.parse(sig)[0]
        self.assertEqual(result, expected)

    # when writing a period type, writing 'whole' before days won't work (worked for months and weeks)
    # def test_parse_sig_period_whole_days(self):
    #     sig = "Take 2 tabs of amoxicillin 500mg every 12 days for 10 whole days"
    #     expected = StructuredSig(drug="amoxicillin", form="tab", strength="500mg", frequencyType="Day", interval=12, 
    #                              singleDosageAmount=2.0, periodType="Day", periodAmount=10, takeAsNeeded=False)
    #     result = self.sig_parser.parse(sig)[0]
    #     self.assertEqual(result, expected)
    
    # can't parse year period type
    # def test_parse_sig_period_year(self):
    #     sig = "Take 2 tabs of amoxicillin 500mg every 12 days for 2 years"
    #     expected = StructuredSig(drug="amoxicillin", form="tab", strength="500mg", frequencyType="Day", interval=12, 
    #                              singleDosageAmount=2.0, periodType="Year", periodAmount=2, takeAsNeeded=False)
    #     result = self.sig_parser.parse(sig)[0]
    #     self.assertEqual(result, expected)

    # we get dosageAmount of 1 instead of 2. 
    # You can also try later writing 'before breakfast and dinner' or when waking up and before sleep'
    # def test_parse_sig_frequency_by_events_of_day(self):
    #     sig = "Take 1 tablet of amoxicillin 500mg each morning and evening"
    #     expected = StructuredSig(drug="amoxicillin", form="tablet", strength="500mg", frequencyType="Day", interval=1, 
    #                              singleDosageAmount=2.0, periodType=None, periodAmount=None, takeAsNeeded=False)
    #     result = self.sig_parser.parse(sig)[0]
    #     self.assertEqual(result, expected)

    def test_parse_sig_period_year(self):
        sig = "Take 2 tabs of amoxicillin 500mg every 12 days for 2 years"
        expected = StructuredSig(drug="amoxicillin", form="tab", strength="500mg", frequencyType="Day", interval=12, 
                                 singleDosageAmount=2.0, periodType="Year", periodAmount=2, takeAsNeeded=False)
        result = self.sig_parser.parse(sig)[0]
        self.assertEqual(result, expected)

    def test_parse_no_drug(self):
        sig = "Take 1 pill 3 times a day"
        expected = StructuredSig(drug=None, form='pill', strength=None, frequencyType="Day", interval=3, 
                                 singleDosageAmount=1.0, periodType=None, periodAmount=None, takeAsNeeded=False)
        result = self.sig_parser.parse(sig)[0]
        self.assertEqual(result, expected)

    def test_parse_sig_text_and_regular_numbers(self):
        sig = "Take two tablets of ibuprofen 3 times every week"
        expected = StructuredSig(drug='ibuprofen', form='tablet', strength=None, frequencyType="Week", interval=3, 
                                 singleDosageAmount=2.0, periodType=None, periodAmount=None, takeAsNeeded=False)
        result = self.sig_parser.parse(sig)[0]
        self.assertEqual(result, expected)

    def test_unprocessed_sig(self):
        sig = "INHALE 2 puffs EVERY DAY"
        expected = StructuredSig(drug=None, form='puff', strength=None, frequencyType="Day", interval=1, 
                                 singleDosageAmount=2.0, periodType=None, periodAmount=None, takeAsNeeded=False)
        result = self.sig_parser.parse(sig)[0]
        self.assertEqual(result, expected)

    def test_as_needed(self):
        sig = "TAKE 1 TABLET BY MOUTH EVERY 6 HOURS AS NEEDED FOR PAIN"
        expected = StructuredSig(drug=None, form='tablet', strength=None, frequencyType="Hour", interval=6, 
                                 singleDosageAmount=1.0, periodType=None, periodAmount=None, takeAsNeeded=True)
        result = self.sig_parser.parse(sig)[0]
        self.assertEqual(result, expected)
    
    # as needed after period type won't be parsed
    # def test_as_needed_after_period(self):
    #     sig = "TAKE 1 TABLET BY MOUTH EVERY 6 HOURS for 2 whole months as needed FOR PAIN"
    #     expected = StructuredSig(drug=None, form='tablet', strength=None, frequencyType="Hour", interval=6, 
    #                              singleDosageAmount=1.0, periodType="Month", periodAmount=2, takeAsNeeded=True)
    #     result = self.sig_parser.parse(sig)[0]
    #     self.assertEqual(result, expected)

    def test_parse_sig_short_form(self):
        sig = "Take 1 tab of Benadryl 3 times a day"
        expected = StructuredSig(drug='benadryl', form='tablet', strength=None, frequencyType="Day", interval=3, 
                                 singleDosageAmount=1.0, periodType=None, periodAmount=None, takeAsNeeded=False)
        result = self.sig_parser.parse(sig)[0]
        self.assertEqual(result, expected)

    def test_parse_sig_no_form(self):
        sig = "Take 1 codeine 3 times a day"
        expected = StructuredSig(drug='codeine', form=None, strength=None, frequencyType="Day", interval=3, 
                                 singleDosageAmount=1.0, periodType=None, periodAmount=None, takeAsNeeded=False)
        result = self.sig_parser.parse(sig)[0]
        self.assertEqual(result, expected)

    def test_parse_sig_every_other_time_unit(self):
        sig = "TAKE 1 TABLET BY MOUTH EVERY OTHER DAY"
        expected = StructuredSig(drug=None, form='tablet', strength=None, frequencyType="Day", interval=2, 
                                 singleDosageAmount=1.0, periodType=None, periodAmount=None, takeAsNeeded=False)
        result = self.sig_parser.parse(sig)[0]
        self.assertEqual(result, expected)

    def test_parse_sig_latin(self):
        sig = "1 TAB of BENADRYL BID"
        expected = StructuredSig(drug="benadryl", form='tablet', strength=None, frequencyType="Day", interval=2, 
                                 singleDosageAmount=1.0, periodType=None, periodAmount=None, takeAsNeeded=False)
        result = self.sig_parser.parse(sig)[0]
        self.assertEqual(result, expected)

    def test_parse_sig_capsules(self):
        sig = "Take 2 capsules of amoxicillin 500mg"
        expected = StructuredSig(drug="amoxicillin", form="capsule", strength="500mg", frequencyType=None, interval=None, 
                                 singleDosageAmount=2.0, periodType=None, periodAmount=None, takeAsNeeded=False)
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
    
    def test_parse_multiple_instructions4(self):
        sig = "take two tablets of benadryl every two days, 1 tablet of aspirin every week for 1 month and 1 tablet of ibuprofen every month"
        first_expected = StructuredSig(drug="benadryl", form="tablet", strength=None, frequencyType="Day", interval=2,
                                       singleDosageAmount=2.0, periodType=None, periodAmount=None, takeAsNeeded=False)
        second_expected = StructuredSig(drug="aspirin", form="tablet", strength=None, frequencyType='Week', interval=1,
                                        singleDosageAmount=1.0, periodType='Month', periodAmount=1, takeAsNeeded=False)
        third_expected = StructuredSig(drug="ibuprofen", form="tablet", strength=None, frequencyType='Month', interval=1,
                                       singleDosageAmount=1.0, periodType=None, periodAmount=None, takeAsNeeded=False)
        result = self.sig_parser.parse(sig)
        expected = [first_expected, second_expected, third_expected]
        self.assertEqual(result, expected)
    
    def test_parse_multiple_instructions5(self):
        sig = "take two tablets of benadryl every two days, 1 tablet of aspirin every week as needde and 1 tablet of ibuprofen every month for 5 months"
        first_expected = StructuredSig(drug="benadryl", form="tablet", strength=None, frequencyType="Day", interval=2,
                                       singleDosageAmount=2.0, periodType=None, periodAmount=None, takeAsNeeded=False)
        second_expected = StructuredSig(drug="aspirin", form="tablet", strength=None, frequencyType='Week', interval=1,
                                        singleDosageAmount=1.0, periodType=None, periodAmount=None, takeAsNeeded=True)
        third_expected = StructuredSig(drug="ibuprofen", form="tablet", strength=None, frequencyType='Month', interval=1,
                                       singleDosageAmount=1.0, periodType="Month", periodAmount=5, takeAsNeeded=False)
        result = self.sig_parser.parse(sig)
        expected = [first_expected, second_expected, third_expected]
        self.assertEqual(result, expected)
    
    # writing 3 drugs, with the 3rd one without a name, we get the name of the first drug instead of the second drug
    # def test_parse_multiple_instructions6(self):
    #     sig = "take two tablets of benadryl every two days, 1 tablet of aspirin every week as needde and than 1 tablet every month for 5 months"
    #     first_expected = StructuredSig(drug="benadryl", form="tablet", strength=None, frequencyType="Day", interval=2,
    #                                    singleDosageAmount=2.0, periodType=None, periodAmount=None, takeAsNeeded=False)
    #     second_expected = StructuredSig(drug="aspirin", form="tablet", strength=None, frequencyType='Week', interval=1,
    #                                     singleDosageAmount=1.0, periodType=None, periodAmount=None, takeAsNeeded=True)
    #     third_expected = StructuredSig(drug="aspirin", form="tablet", strength=None, frequencyType='Month', interval=1,
    #                                    singleDosageAmount=1.0, periodType="Month", periodAmount=5, takeAsNeeded=False)
    #     result = self.sig_parser.parse(sig)
    #     expected = [first_expected, second_expected, third_expected]
    #     self.assertEqual(result, expected)

    def test_autocorrect_with_a_sentence(self):
        sig = "So, after examining you i want you to tAEk 1 plil of Propecia 5mg two tmies a day"
        expected = StructuredSig(drug='propecia', form='pill', strength="5mg", frequencyType="Day", interval=2,
                                 singleDosageAmount=1.0, periodType=None, periodAmount=None, takeAsNeeded=False)
        result = self.sig_parser.parse(sig)[0]
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

    def test_autocorrect_and__pre_process8(self):
        sig = "tAEk 1 plil of Propecia 5mg two tmies a day"
        expected = StructuredSig(drug='propecia', form='pill', strength="5mg", frequencyType="Day", interval=2,
                                 singleDosageAmount=1.0, periodType=None, periodAmount=None, takeAsNeeded=False)
        result = self.sig_parser.parse(sig)[0]
        self.assertEqual(result, expected)
    
    def test_autocorrect_and__pre_process9(self):
        sig = "I submit for you 1 plil of Propecia 5mg htree tmies a day as needde for 2 months"
        expected = StructuredSig(drug='propecia', form='pill', strength="5mg", frequencyType="Day", interval=3,
                                 singleDosageAmount=1.0, periodType="Month", periodAmount=2, takeAsNeeded=True)
        result = self.sig_parser.parse(sig)[0]
        self.assertEqual(result, expected)
        
    def test_autocorrect_and__pre_process10(self):
        sig = "I submti for you 1 plil of Propecia 5mg three tmies a day"
        expected = StructuredSig(drug='propecia', form='pill', strength="5mg", frequencyType="Day", interval=3,
                                 singleDosageAmount=1.0, periodType=None, periodAmount=None, takeAsNeeded=False)
        result = self.sig_parser.parse(sig)[0]
        self.assertEqual(result, expected)
    
    def test_autocorrect_and__pre_process11(self):
        sig = "I write for you 1 plil of proPeCia 5mg three tmies a day"
        expected = StructuredSig(drug='propecia', form='pill', strength="5mg", frequencyType="Day", interval=3,
                                 singleDosageAmount=1.0, periodType=None, periodAmount=None, takeAsNeeded=False)
        result = self.sig_parser.parse(sig)[0]
        self.assertEqual(result, expected)