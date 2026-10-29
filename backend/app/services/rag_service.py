import os
import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
import numpy as np
import faiss

from app.core.config import settings
from app.models.schemas import RetrievedExemplar

logger = logging.getLogger("RAGService")

class MiniLMEmbedder:
    """
    Sentence-Transformers all-MiniLM-L6-v2 Embedder with fast local fallback.
    """
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.model = None
        self.dimension = 384
        self._initialized = False

    def _ensure_model(self):
        if self._initialized:
            return
        self._initialized = True
        try:
            from sentence_transformers import SentenceTransformer
            os.environ["HF_HUB_OFFLINE"] = "1"
            os.environ["TRANSFORMERS_OFFLINE"] = "1"
            logger.info(f"Loading local SentenceTransformer '{self.model_name}'...")
            self.model = SentenceTransformer(self.model_name, local_files_only=True)
            if hasattr(self.model, "get_embedding_dimension"):
                self.dimension = self.model.get_embedding_dimension()
            else:
                self.dimension = self.model.get_sentence_embedding_dimension()
            logger.info(f"SentenceTransformer loaded successfully. Dimension: {self.dimension}")
        except Exception as e:
            logger.warning(f"SentenceTransformer offline load failed ({e}). Using deterministic lexical-semantic projection embedder.")
            self.model = None
            self.dimension = 384

    def encode(self, texts: List[str]) -> np.ndarray:
        self._ensure_model()
        if self.model is not None:
            try:
                embeddings = self.model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
                # Ensure float32 and 2D
                if len(embeddings.shape) == 1:
                    embeddings = embeddings.reshape(1, -1)
                embeddings = embeddings.astype(np.float32)
                faiss.normalize_L2(embeddings)
                return embeddings
            except Exception as e:
                logger.error(f"Inference error in SentenceTransformer: {e}. Falling back to semantic projection.")

        # Deterministic semantic hash projection (384-dim)
        embeddings = np.zeros((len(texts), self.dimension), dtype=np.float32)
        for i, text in enumerate(texts):
            words = text.lower().split()
            for word in words:
                # Deterministic word hash
                seed = sum(ord(c) * (31 ** idx) for idx, c in enumerate(word[:10])) % (2**31 - 1)
                rng = np.random.RandomState(seed)
                word_vec = rng.randn(self.dimension).astype(np.float32)
                embeddings[i] += word_vec
            norm = np.linalg.norm(embeddings[i])
            if norm > 0:
                embeddings[i] /= norm
            else:
                embeddings[i, 0] = 1.0
        return embeddings


class RAGService:
    def __init__(self):
        self.embedder = MiniLMEmbedder(settings.EMBEDDING_MODEL_NAME)
        self.index: Optional[faiss.IndexFlatIP] = None
        self.records: List[Dict[str, Any]] = []
        self._initialize_index()

    def _initialize_index(self):
        index_file = Path(settings.FAISS_INDEX_PATH)
        meta_file = Path(settings.FAISS_METADATA_PATH)

        if index_file.exists() and meta_file.exists():
            try:
                self.index = faiss.read_index(str(index_file))
                with open(meta_file, "r", encoding="utf-8") as f:
                    self.records = json.load(f)
                logger.info(f"Loaded existing FAISS index with {self.index.ntotal} records.")
                return
            except Exception as e:
                logger.warning(f"Could not load saved index: {e}. Rebuilding...")

        self.rebuild_index()

    def rebuild_index(self) -> int:
        """
        Builds FAISS index strictly from train and val partitions (NEVER test).
        """
        corpus_dir = Path(settings.CORPUS_DIR)
        all_records = []

        for filename in ["isl_csltr_curated.json", "cislr_curated.json"]:
            filepath = corpus_dir / filename
            if filepath.exists():
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for item in data:
                        # CRITICAL: Exclude test partition to preserve scientific evaluation validity!
                        if item.get("split") != "test":
                            all_records.append(item)

        if not all_records:
            logger.warning("No corpus records found to index.")
            self.index = faiss.IndexFlatIP(self.embedder.dimension)
            self.records = []
            return 0

        # Encode normalized English and source sentences
        sentences_to_encode = [
            f"{r.get('source_text', '')} {r.get('normalized_english', '')}".strip()
            for r in all_records
        ]
        
        vectors = self.embedder.encode(sentences_to_encode)
        
        index = faiss.IndexFlatIP(self.embedder.dimension)
        index.add(vectors)

        self.index = index
        self.records = all_records

        # Save to disk
        try:
            Path(settings.FAISS_INDEX_PATH).parent.mkdir(parents=True, exist_ok=True)
            faiss.write_index(index, settings.FAISS_INDEX_PATH)
            with open(settings.FAISS_METADATA_PATH, "w", encoding="utf-8") as f:
                json.dump(all_records, f, indent=2, ensure_ascii=False)
            logger.info(f"Built and persisted FAISS index with {len(all_records)} exemplars.")
        except Exception as e:
            logger.error(f"Error saving FAISS index to disk: {e}")

        return len(all_records)

    def query(self, text: str, top_k: int = 3, threshold: float = 0.50) -> List[RetrievedExemplar]:
        if self.index is None or self.index.ntotal == 0 or not text.strip():
            return []

        query_vec = self.embedder.encode([text])
        k = min(top_k, self.index.ntotal)
        scores, indices = self.index.search(query_vec, k)

        results: List[RetrievedExemplar] = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < 0 or idx >= len(self.records):
                continue
            sim = float(score)
            if sim >= threshold:
                rec = self.records[idx]
                results.append(
                    RetrievedExemplar(
                        id=rec.get("id", f"rec_{idx}"),
                        dataset=rec.get("dataset", "UNKNOWN"),
                        source_text=rec.get("source_text", ""),
                        normalized_english=rec.get("normalized_english", ""),
                        gloss_sequence=rec.get("gloss_sequence", []),
                        similarity_score=round(sim, 4),
                        grammar_annotations=rec.get("grammar_annotations")
                    )
                )
        return results

    @property
    def total_records(self) -> int:
        return self.index.ntotal if self.index is not None else 0

rag_service = RAGService()
