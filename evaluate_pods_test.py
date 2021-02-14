import unittest

from pod_test_data import pod_test_data, expected_eval_result
from main import evaluate_pod


class TestEvaluatePods(unittest.TestCase):

    def test_evaluate_pods(self, pod=pod_test_data):
        eval_result = evaluate_pod(pod)
        expected_result = expected_eval_result
        self.assertEqual(eval_result, expected_result, "Should be equal to the expected result")


if __name__ == "__main__":
    unittest.main()