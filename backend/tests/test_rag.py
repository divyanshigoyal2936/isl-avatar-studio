import unittest
from app.services.rag_service import rag_service

class TestRAGService(unittest.TestCase):
    def test_rag_index_contains_records(self):
        self.assertGreater(rag_service.total_records, 0)

    def test_rag_query_matching(self):
        results = rag_service.query("where is the hospital", top_k=3, threshold=0.40)
        self.assertGreater(len(results), 0)
        # Verify similarity is normalized cosine <= 1.0
        for r in results:
            self.assertLessEqual(r.similarity_score, 1.0)
            self.assertGreaterEqual(r.similarity_score, 0.40)
            self.assertIsInstance(r.gloss_sequence, list)

    def test_rag_query_empty_returns_empty(self):
        results = rag_service.query("", top_k=3)
        self.assertEqual(results, [])

    def test_test_split_exclusion(self):
        # Verify no record indexed has split == 'test'
        for rec in rag_service.records:
            self.assertNotEqual(rec.get("split"), "test", f"Data leakage found: {rec.get('id')}")

if __name__ == "__main__":
    unittest.main()
