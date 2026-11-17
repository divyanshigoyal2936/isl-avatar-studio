import json
import time
import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

from app.core.config import settings
from app.services.rag_service import rag_service
from app.services.gloss_service import gloss_service
from app.services.animation_service import animation_service
from app.models.schemas import EvaluationResponse, EvaluationMetrics

class EvaluationService:
    def __init__(self):
        self.benchmark_path = Path(settings.CORPUS_DIR) / "benchmark_eval.json"

    def run_evaluation(self, use_rag: bool = True, test_limit: Optional[int] = None) -> EvaluationResponse:
        if not self.benchmark_path.exists():
            raise FileNotFoundError(f"Benchmark evaluation file not found at {self.benchmark_path}")

        with open(self.benchmark_path, "r", encoding="utf-8") as f:
            test_samples = json.load(f)

        if test_limit and test_limit > 0:
            test_samples = test_samples[:test_limit]

        total_samples = len(test_samples)
        if total_samples == 0:
            raise ValueError("No test samples available for evaluation.")

        r1_hits = 0
        r3_hits = 0
        exact_matches = 0
        precisions = []
        recalls = []
        f1s = []
        bleu1_scores = []
        coverage_scores = []
        latencies = []

        sample_predictions: List[Dict[str, Any]] = []

        for sample in test_samples:
            t0 = time.perf_counter()
            query_text = sample.get("normalized_english") or sample.get("source_text", "")
            gold_gloss = sample.get("gold_gloss", [])

            # Retrieval
            retrieved = rag_service.query(query_text, top_k=3, threshold=0.30)
            
            # Check retrieval hits against domain or shared key tokens
            gold_set = set(gold_gloss)
            if retrieved:
                top1_tokens = set(retrieved[0].gloss_sequence)
                if len(gold_set.intersection(top1_tokens)) > 0:
                    r1_hits += 1
                all_r3_tokens = set().union(*[set(r.gloss_sequence) for r in retrieved])
                if len(gold_set.intersection(all_r3_tokens)) > 0:
                    r3_hits += 1

            # Gloss Generation
            pred_gloss, explanation, _, _ = gloss_service.generate_gloss(
                normalized_english=query_text,
                retrieved_exemplars=retrieved,
                use_rag=use_rag
            )

            latency_ms = (time.perf_counter() - t0) * 1000.0
            latencies.append(latency_ms)

            # Metrics
            # Exact Match
            em = 1.0 if pred_gloss == gold_gloss else 0.0
            exact_matches += em

            # Token F1
            pred_set = set(pred_gloss)
            intersection = gold_set.intersection(pred_set)
            p = len(intersection) / len(pred_set) if pred_set else 0.0
            r = len(intersection) / len(gold_set) if gold_set else 0.0
            f1 = (2 * p * r) / (p + r) if (p + r) > 0 else 0.0

            precisions.append(p)
            recalls.append(r)
            f1s.append(f1)

            # BLEU-1
            overlap_count = sum(min(pred_gloss.count(t), gold_gloss.count(t)) for t in set(pred_gloss))
            bleu1 = overlap_count / len(pred_gloss) if pred_gloss else 0.0
            bleu1_scores.append(bleu1)

            # Animation coverage
            _, supported, _, cov_pct, _, _ = animation_service.schedule_sequence(pred_gloss)
            coverage_scores.append(cov_pct)

            sample_predictions.append({
                "id": sample.get("id"),
                "source_text": sample.get("source_text"),
                "gold_gloss": gold_gloss,
                "predicted_gloss": pred_gloss,
                "exact_match": bool(em),
                "token_f1": round(f1, 3),
                "retrieved_exemplar_id": retrieved[0].id if retrieved else None,
                "retrieval_similarity": retrieved[0].similarity_score if retrieved else 0.0
            })

        metrics = EvaluationMetrics(
            total_test_samples=total_samples,
            recall_at_1=round(r1_hits / total_samples, 3),
            recall_at_3=round(r3_hits / total_samples, 3),
            gloss_exact_match=round(exact_matches / total_samples, 3),
            gloss_token_f1=round(sum(f1s) / total_samples, 3),
            gloss_token_precision=round(sum(precisions) / total_samples, 3),
            gloss_token_recall=round(sum(recalls) / total_samples, 3),
            bleu_1=round(sum(bleu1_scores) / total_samples, 3),
            animation_coverage_pct=round(sum(coverage_scores) / total_samples, 1),
            avg_latency_ms=round(sum(latencies) / total_samples, 2)
        )

        mode_name = "RAG_Assisted" if use_rag else "Zero_Shot_Baseline"
        return EvaluationResponse(
            mode=mode_name,
            timestamp=datetime.datetime.utcnow().isoformat() + "Z",
            metrics=metrics,
            sample_predictions=sample_predictions,
            methodology_notes=(
                "Evaluation evaluated against held-out benchmark split strictly isolated from the FAISS retrieval index. "
                "Metrics report token overlap F1, strict Exact Match, Recall@k of retrieved corpus exemplars, "
                "BLEU-1 supplementary text alignment, verified 3D animation coverage, and stage latency."
            ),
            limitations=(
                "BLEU and token F1 are supplementary string/token overlap metrics and do not fully capture spatial "
                "co-reference, signing space utilization, or non-manual facial grammatical subtleties in 3D ISL. "
                "Human evaluation by certified ISL interpreters remains the definitive standard."
            )
        )

evaluation_service = EvaluationService()
