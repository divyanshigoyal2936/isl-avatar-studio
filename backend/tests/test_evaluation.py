import unittest
from app.services.evaluation_service import evaluation_service

class TestEvaluationService(unittest.TestCase):
    def test_run_evaluation_rag_mode(self):
        res = evaluation_service.run_evaluation(use_rag=True, test_limit=3)
        self.assertEqual(res.mode, "RAG_Assisted")
        self.assertEqual(res.metrics.total_test_samples, 3)
        self.assertGreaterEqual(res.metrics.gloss_token_f1, 0.0)
        self.assertLessEqual(res.metrics.gloss_token_f1, 1.0)
        self.assertGreater(res.metrics.animation_coverage_pct, 0.0)
        self.assertGreater(res.metrics.avg_latency_ms, 0.0)
        self.assertEqual(len(res.sample_predictions), 3)

    def test_run_evaluation_baseline_mode(self):
        res = evaluation_service.run_evaluation(use_rag=False, test_limit=3)
        self.assertEqual(res.mode, "Zero_Shot_Baseline")
        self.assertEqual(res.metrics.total_test_samples, 3)

if __name__ == "__main__":
    unittest.main()
