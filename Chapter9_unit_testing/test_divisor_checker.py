import unittest
from divisor_app.divisor_checker import DivisorChecker


class TestDivisorChecker(unittest.TestCase):

    def setUp(self):
        """This runs before every test case."""
        self.divisor_checker = DivisorChecker()

    def test_count_valid_n_positive_case(self):
        """Test with a case where divisors of n and n+1 are equal."""
        # Example: For k=3, the valid n values are [2]
        result = self.divisor_checker.count_valid_n(3)
        self.assertEqual(result, 1, "Expected 1 valid n value.")

    def test_count_valid_n_multiple_valid(self):
        """Test case with multiple valid n values."""
        # Example: For k=15, there are 2 valid n values [2, 14]
        result = self.divisor_checker.count_valid_n(15)
        self.assertEqual(result, 2, "Expected 2 valid n values.")

    def test_count_valid_n_large_input(self):
        """Test with a larger input to check efficiency and correctness."""
        # Example: For k=100, expect 15 valid n values
        result = self.divisor_checker.count_valid_n(100)
        self.assertEqual(result, 15, "Expected 15 valid n values.")

    def test_count_valid_n_no_valid_case(self):
        """Test case where no valid n values exist."""
        # Example: For k=1, there are no valid n values
        result = self.divisor_checker.count_valid_n(1)
        self.assertEqual(result, 0, "Expected 0 valid n values.")

    def test_count_valid_n_edge_case(self):
        """Test with an edge case where the range is minimal (k=2)."""
        result = self.divisor_checker.count_valid_n(2)
        self.assertEqual(result, 0, "Expected 0 valid n values.")

    def test_count_valid_n_large_range(self):
        """Test case with a large range, edge case."""
        result = self.divisor_checker.count_valid_n(1000)
        # This is a large input, but we expect a number of valid cases.
        self.assertIsInstance(result, int, "Expected integer result.")


if __name__ == "__main__":
    unittest.main()
