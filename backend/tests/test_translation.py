import unittest
from app.services.translation_service import translation_service

class TestTranslationService(unittest.TestCase):
    def test_language_detection(self):
        self.assertEqual(translation_service.detect_language("Hello world"), "en")
        self.assertEqual(translation_service.detect_language("नमस्ते, आप कैसे हैं?"), "hi")
        self.assertEqual(translation_service.detect_language("மருத்துவர் எங்கே?"), "ta")
        self.assertEqual(translation_service.detect_language("నాకు భోజనం కావాలి"), "te")
        self.assertEqual(translation_service.detect_language("আজ আমি স্কুলে যাব না"), "bn")
        self.assertEqual(translation_service.detect_language("मला पाणी पाहिजे"), "mr")

    def test_semantic_analysis_entities(self):
        res = translation_service.normalize_and_analyze("Where is the hospital?")
        self.assertEqual(res.detected_language, "en")
        self.assertTrue(res.has_question)
        entity_types = [e.entity_type for e in res.entities]
        self.assertIn("QUESTION", entity_types)
        self.assertIn("OBJECT", entity_types)

    def test_negation_detection(self):
        res = translation_service.normalize_and_analyze("आज मैं स्कूल नहीं जाऊंगा", source_language="hi")
        self.assertEqual(res.detected_language, "hi")
        self.assertTrue(res.has_negation)
        self.assertEqual(res.time_marker, "TODAY")

    def test_empty_input_raises_error(self):
        with self.assertRaises(ValueError):
            translation_service.normalize_and_analyze("   ")

if __name__ == "__main__":
    unittest.main()
