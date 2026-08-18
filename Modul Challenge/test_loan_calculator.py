import unittest
from loan_calculator import calculate_ltv, is_ltv_eligible


class LoanToValueTest(unittest.TestCase):

    def test_calculate_ltv_should_return_correct_percentage(self):
        loan_amount = 160_000_000
        asset_value = 200_000_000
        actual = calculate_ltv(loan_amount, asset_value)
        self.assertEqual(actual, 80.0)

    def test_asset_value_zero_should_raise_error(self):
        with self.assertRaises(ValueError):
            calculate_ltv(100_000_000, 0)

    def test_ltv_below_limit_should_be_eligible(self):
        self.assertTrue(is_ltv_eligible(140_000_000, 200_000_000))

    def test_ltv_exactly_on_limit_should_be_eligible(self):
        self.assertTrue(is_ltv_eligible(160_000_000, 200_000_000))

    def test_ltv_above_limit_should_not_be_eligible(self):
        self.assertFalse(is_ltv_eligible(170_000_000, 200_000_000))


if __name__ == "__main__":
    unittest.main()