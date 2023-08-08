import random
import unittest

from hypothesis import given
from hypothesis import settings
from hypothesis import strategies as st
from parsigs.parse_sig_api import SigParser
from parsigs.parse_sig_api import StructuredSig


class TestParseSigApi(unittest.TestCase):
    parser = SigParser()

    @given(st.integers(min_value=1, max_value=30))
    @settings(max_examples=30)
    def test_parse_sig_strength(self, strength):
        sig = f"Take 1 tablet of ibuprofen {strength}mg 3 times every day for 10 weeks"
        expected = [
            StructuredSig(
                drug="ibuprofen",
                form="tablet",
                strength=f"{strength}mg",
                frequency_type="Day",
                interval=3,
                single_dosage_amount=1.0,
                period_type="Week",
                period_amount=10,
                take_as_needed=False,
            ),
        ]
        result = self.parser.parse(sig)
        self.assertEqual(result, expected)

    @given(
        count_tabs=st.integers(min_value=1, max_value=5),
        count_mg=st.integers(min_value=300, max_value=500),
        count_every_days=st.integers(min_value=3, max_value=10),
        count_days=st.integers(min_value=4, max_value=10),
    )
    def test_parse_sig_period(
        self, count_tabs: int, count_mg: int, count_every_days: int, count_days: int,
    ):
        """
        Test parsing prescription instructions with period values.

        This test generates random values for the number of tabs, mg amount,
        frequency interval, and period days/weeks/months.

        It constructs an input string using these values, parses it with SigParser,
        and asserts that the parsed StructuredSig matches the expected parameters.

        Args:
          count_tabs: Random integer from 1 to 5, number of tabs in prescription
          count_mg: Random integer from 2 to 10, mg amount of medication
          count_every_days: Random integer from 3 to 10, frequency interval in days
          count_days: Random integer from 4 to 10, period amount in days/weeks/months

        Returns:
          bool: True if parsed result matches expected, False otherwise
        """

        period_dict = {"days": "Day", "weeks": "Week", "months": "Month"}

        # Generate random period type of days/weeks/months
        period_for_string, period_for_obj = random.choice(list(period_dict.items()))

        # Construct prescription string using random values
        sig = f"Take {count_tabs} tablets of amoxicillin {count_mg}mg every {count_every_days} days for {count_days} {period_for_string}"

        # Expected StructuredSig using random values
        expected = [
            StructuredSig(
                drug="amoxicillin",
                form="tablet",
                strength=f"{count_mg}mg",
                frequency_type="Day",
                interval=count_every_days,
                single_dosage_amount=float(count_tabs),
                period_type=period_for_obj,
                period_amount=count_days,
                take_as_needed=False,
            ),
        ]

        # Parse prescription string
        result = self.parser.parse(sig)

        # Assert parsed result matches expected
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
