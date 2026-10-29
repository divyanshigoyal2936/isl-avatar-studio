import unittest
import asyncio
from app.models.schemas import (
    TranslateRequest, SignGenerateRequest, SignPreviewRequest, RAGQueryRequest
)
from app.api.health import get_health
from app.api.translate import get_supported_languages, translate_and_normalize
from app.api.sign import generate_isl_sign_sequence, preview_sign_clip, get_sign_metadata, get_animation_manifest
from app.api.rag import query_rag_index, rebuild_rag_index
from app.database.db import get_db

class TestAPIEndpoints(unittest.TestCase):
    def setUp(self):
        self.db = next(get_db())

    def tearDown(self):
        self.db.close()

    def test_health_endpoint(self):
        data = get_health()
        self.assertEqual(data.status, "healthy")
        self.assertIn("embedding_model", data.models)
        self.assertIn("total_indexed_exemplars", data.rag_index)

    def test_languages_endpoint(self):
        data = get_supported_languages()
        self.assertGreater(len(data.supported_languages), 5)
        codes = [lang.code for lang in data.supported_languages]
        self.assertIn("en", codes)
        self.assertIn("hi", codes)

    def test_translate_endpoint(self):
        req = TranslateRequest(text="Where is the hospital?")
        res = translate_and_normalize(req)
        self.assertEqual(res.detected_language, "en")
        self.assertTrue(res.has_question)
        self.assertIn("hospital", res.normalized_english)

    def test_sign_generate_endpoint(self):
        req = SignGenerateRequest(
            text="Where is the hospital?",
            use_rag=True,
            rag_top_k=3
        )
        res = generate_isl_sign_sequence(req, db=self.db)
        self.assertIsNotNone(res.request_id)
        self.assertIn("HOSPITAL", res.generated_gloss)
        self.assertIn("WHERE", res.generated_gloss)
        self.assertGreater(len(res.scheduled_clips), 0)
        self.assertGreaterEqual(res.animation_coverage_pct, 50.0)
        self.assertGreater(res.total_animation_duration_ms, 1000)

    def test_sign_preview_endpoint(self):
        req = SignPreviewRequest(gloss_token="HELLO")
        res = preview_sign_clip(req)
        self.assertEqual(res.gloss_token, "HELLO")
        self.assertTrue(res.is_verified)
        self.assertEqual(res.hand_dominance, "bimanual_symmetric")

    def test_manifest_endpoint(self):
        data = get_animation_manifest()
        self.assertIn("signs", data)
        self.assertGreaterEqual(data["total_verified_signs"], 20)

    def test_rag_query_endpoint(self):
        req = RAGQueryRequest(query="hospital doctor", top_k=2)
        res = query_rag_index(req)
        self.assertGreater(len(res.results), 0)
        self.assertGreater(res.total_index_size, 0)

    def test_empty_input_validation(self):
        req = SignGenerateRequest(text="")
        with self.assertRaises(Exception):
            generate_isl_sign_sequence(req, db=self.db)

if __name__ == "__main__":
    unittest.main()
