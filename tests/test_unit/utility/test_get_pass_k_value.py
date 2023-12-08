import unittest
import sys
from pyprojroot import here
sys.path.append(str(here()))

from utility.get_pass_k_value import get_pass_k_value


class TestGetPassKValue(unittest.TestCase):

    def test_pass_k_value_found(self):
        output_text = """
        {'pass@1': 0.3170731707317073}
        """
        result = get_pass_k_value(output_text)
        self.assertEqual(result, "pass@1: 0.3170731707317073")

    def test_pass_k_value_not_found(self):
        output_text = """
        No pass@k value here
        """
        result = get_pass_k_value(output_text)
        self.assertEqual(result, "pass@k value not found")

if __name__ == '__main__':
    unittest.main()
