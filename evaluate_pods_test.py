import unittest

from pods_list_test_data import pods_list_test_data, expected_eval_result
from main import evaluate_pods


class TestEvaluatePods(unittest.TestCase):

    def test_evaluate_pods(self, pods_list=pods_list_test_data):
        eval_result = evaluate_pods(pods_list)
        expected_result = expected_eval_result
        self.assertEqual(eval_result, expected_result, "Should be equal to the expected result")


if __name__ == "__main__":
    unittest.main()