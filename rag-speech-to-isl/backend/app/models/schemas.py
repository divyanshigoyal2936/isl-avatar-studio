from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

# --- Health ---
class HealthResponse(BaseModel):
    status: str
    app_name: str
    version: str
    models: Dict[str, Any]
    rag_index: Dict[str, Any]
    animation_library: Dict[str, Any]
    database: str

# --- Languages ---
class LanguageInfo(BaseModel):
    code: str
    name: str
    native_name: str
    stt_status: str  # "verified", "supported", "fallback"
    translation_status: str

class LanguagesResponse(BaseModel):
    supported_languages: List[LanguageInfo]
    default_language: str

# --- Speech to text ---
class TranscribeResponse(BaseModel):
    transcript: str
    detected_language: str
    confidence: float
    duration_seconds: float
    provider: str
    sample_rate_hz: Optional[int] = 16000

# --- Translation / Normalization ---
class SemanticEntity(BaseModel):
    entity_type: str  # "TIME", "QUESTION", "NEGATION", "SUBJECT", "OBJECT", "ACTION"
    text: str
    isl_role: str

class TranslateRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=500)
    source_language: Optional[str] = "auto"

class TranslateResponse(BaseModel):
    original_text: str
    detected_language: str
    normalized_english: str
    entities: List[SemanticEntity]
    has_question: bool
    has_negation: bool
    time_marker: Optional[str] = None

# --- RAG ---
class RetrievedExemplar(BaseModel):
    id: str
    dataset: str
    source_text: str
    normalized_english: str
    gloss_sequence: List[str]
    similarity_score: float
    grammar_annotations: Optional[Dict[str, Any]] = None

class RAGQueryRequest(BaseModel):
    query: str
    top_k: Optional[int] = 3
    threshold: Optional[float] = 0.50

class RAGQueryResponse(BaseModel):
    query: str
    top_k: int
    threshold: float
    results: List[RetrievedExemplar]
    total_index_size: int

# --- Sign & Animation ---
class GlossTokenDetail(BaseModel):
    token: str
    syntax_role: str  # "TIME", "TOPIC", "SUBJECT", "OBJECT", "VERB", "NEGATION", "QUESTION"
    is_verified: bool
    description: Optional[str] = None
    fallback_fingerspelling: bool = False

class ScheduledClip(BaseModel):
    clip_id: str
    gloss_token: str
    start_time_ms: int
    duration_ms: int
    end_time_ms: int
    transition_in_ms: int
    transition_out_ms: int
    hand_dominance: str
    hand_shape: str
    palm_orientation: str
    signing_space: str
    movement_type: str
    non_manual_markers: Dict[str, str]
    is_verified: bool
    joint_targets: Optional[Dict[str, Any]] = None
    description: Optional[str] = None

class SignGenerateRequest(BaseModel):
    text: Optional[str] = None
    language: Optional[str] = "auto"
    use_rag: bool = True
    rag_top_k: int = 3
    rag_threshold: float = 0.50
    user_consent_history: bool = False

class StageTiming(BaseModel):
    stage: str
    duration_ms: float

class SignGenerateResponse(BaseModel):
    request_id: str
    original_input: str
    detected_language: str
    transcript: str
    normalized_sentence: str
    rag_enabled: bool
    retrieved_exemplars: List[RetrievedExemplar]
    generated_gloss: List[str]
    gloss_details: List[GlossTokenDetail]
    supported_gloss_tokens: List[str]
    unsupported_gloss_tokens: List[str]
    animation_coverage_pct: float
    scheduled_clips: List[ScheduledClip]
    total_animation_duration_ms: int
    explanation: str
    grammar_notes: List[str]
    warnings: List[str]
    timings: List[StageTiming]

class SignPreviewRequest(BaseModel):
    gloss_token: str

# --- Evaluation ---
class EvaluationRequest(BaseModel):
    use_rag: bool = True
    test_limit: Optional[int] = None

class EvaluationMetrics(BaseModel):
    total_test_samples: int
    recall_at_1: float
    recall_at_3: float
    gloss_exact_match: float
    gloss_token_f1: float
    gloss_token_precision: float
    gloss_token_recall: float
    bleu_1: float
    animation_coverage_pct: float
    avg_latency_ms: float

class EvaluationResponse(BaseModel):
    mode: str  # "RAG_Assisted" or "Zero_Shot_Baseline"
    timestamp: str
    metrics: EvaluationMetrics
    sample_predictions: List[Dict[str, Any]]
    methodology_notes: str
    limitations: str
