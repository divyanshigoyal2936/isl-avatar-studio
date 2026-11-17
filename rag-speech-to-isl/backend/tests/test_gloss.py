import unittest
from app.services.gloss_service import gloss_service
from app.models.schemas import RetrievedExemplar

class TestGlossService(unittest.TestCase):
    def test_zero_shot_sov_order(self):
        # "where is the hospital" -> ISL: HOSPITAL WHERE
        gloss_seq, explanation, notes, details = gloss_service.generate_gloss(
            normalized_english="where is the hospital",
            retrieved_exemplars=[],
            use_rag=False
        )
        self.assertIn("HOSPITAL", gloss_seq)
        self.assertIn("WHERE", gloss_seq)
        # Question word must come at the end in ISL
        self.assertEqual(gloss_seq[-1], "WHERE")

    def test_time_marker_at_start(self):
        # "today i will go to hospital" -> TODAY ME HOSPITAL
        gloss_seq, _, _, _ = gloss_service.generate_gloss(
            normalized_english="today i will go to hospital",
            retrieved_exemplars=[],
            use_rag=False
        )
        self.assertEqual(gloss_seq[0], "TODAY")

    def test_negation_placement(self):
        # "today i will not drink water" -> TODAY ... NO
        gloss_seq, _, _, _ = gloss_service.generate_gloss(
            normalized_english="today i will not drink water",
            retrieved_exemplars=[],
            use_rag=False
        )
        self.assertEqual(gloss_seq[0], "TODAY")
        self.assertIn("NO", gloss_seq)

    def test_rag_conditioning_direct_alignment(self):
        mock_exemplar = RetrievedExemplar(
            id="test_001",
            dataset="ISL-CSLTR",
            source_text="Where is the hospital?",
            normalized_english="where is hospital",
            gloss_sequence=["HOSPITAL", "WHERE"],
            similarity_score=0.95,
            grammar_annotations={"word_order": "TOPIC_QUESTION"}
        )
        gloss_seq, explanation, notes, details = gloss_service.generate_gloss(
            normalized_english="where is hospital",
            retrieved_exemplars=[mock_exemplar],
            use_rag=True
        )
        self.assertEqual(gloss_seq, ["HOSPITAL", "WHERE"])
        self.assertIn("RAG direct syntactic alignment", explanation)

if __name__ == "__main__":
    unittest.main()
