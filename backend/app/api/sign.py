import time
import uuid
import json
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.models.schemas import (
    SignGenerateRequest, SignGenerateResponse, SignPreviewRequest,
    ScheduledClip, StageTiming
)
from app.services.translation_service import translation_service
from app.services.rag_service import rag_service
from app.services.gloss_service import gloss_service
from app.services.animation_service import animation_service
from app.database.db import get_db, ConsentedSessionRecord

router = APIRouter(prefix="/api", tags=["Sign Generation"])

@router.post("/sign/generate", response_model=SignGenerateResponse)
def generate_isl_sign_sequence(
    request: SignGenerateRequest,
    db: Session = Depends(get_db)
):
    request_id = str(uuid.uuid4())
    input_text = (request.text or "").strip()
    if not input_text:
        raise HTTPException(status_code=400, detail="Text input cannot be empty.")

    timings = []
    t_start = time.perf_counter()

    # Stage 1 & 2: Language Normalization & Semantic Parsing
    t0 = time.perf_counter()
    trans_res = translation_service.normalize_and_analyze(
        text=input_text,
        source_language=request.language
    )
    timings.append(StageTiming(stage="normalization_and_semantics", duration_ms=round((time.perf_counter() - t0) * 1000, 2)))

    # Stage 3: RAG Retrieval from FAISS Knowledge Base
    t0 = time.perf_counter()
    retrieved_exemplars = []
    if request.use_rag:
        retrieved_exemplars = rag_service.query(
            text=trans_res.normalized_english,
            top_k=request.rag_top_k,
            threshold=request.rag_threshold
        )
    timings.append(StageTiming(stage="rag_faiss_retrieval", duration_ms=round((time.perf_counter() - t0) * 1000, 2)))

    # Stage 4: ISL Gloss Generation
    t0 = time.perf_counter()
    generated_gloss, explanation, grammar_notes, gloss_details = gloss_service.generate_gloss(
        normalized_english=trans_res.normalized_english,
        retrieved_exemplars=retrieved_exemplars,
        use_rag=request.use_rag
    )
    timings.append(StageTiming(stage="isl_gloss_generation", duration_ms=round((time.perf_counter() - t0) * 1000, 2)))

    # Stage 5: Sign Scheduling & Manifest Mapping
    t0 = time.perf_counter()
    scheduled_clips, supported, unsupported, cov_pct, total_dur, warnings = animation_service.schedule_sequence(generated_gloss)
    timings.append(StageTiming(stage="animation_scheduling", duration_ms=round((time.perf_counter() - t0) * 1000, 2)))

    # Consented history storage
    if request.user_consent_history:
        try:
            record = ConsentedSessionRecord(
                session_id=request_id,
                input_text=input_text,
                detected_language=trans_res.detected_language,
                generated_gloss=" ".join(generated_gloss),
                user_consent=True
            )
            db.add(record)
            db.commit()
        except Exception:
            pass

    return SignGenerateResponse(
        request_id=request_id,
        original_input=input_text,
        detected_language=trans_res.detected_language,
        transcript=input_text,
        normalized_sentence=trans_res.normalized_english,
        rag_enabled=request.use_rag,
        retrieved_exemplars=retrieved_exemplars,
        generated_gloss=generated_gloss,
        gloss_details=gloss_details,
        supported_gloss_tokens=supported,
        unsupported_gloss_tokens=unsupported,
        animation_coverage_pct=cov_pct,
        scheduled_clips=scheduled_clips,
        total_animation_duration_ms=total_dur,
        explanation=explanation,
        grammar_notes=grammar_notes,
        warnings=warnings,
        timings=timings
    )

@router.post("/sign/preview", response_model=ScheduledClip)
def preview_sign_clip(request: SignPreviewRequest):
    sign_data = animation_service.get_sign(request.gloss_token)
    if not sign_data:
        raise HTTPException(
            status_code=404,
            detail=f"Sign '{request.gloss_token}' is not certified in the verified ISL library."
        )

    return ScheduledClip(
        clip_id=f"preview_{request.gloss_token}",
        gloss_token=sign_data["gloss_id"],
        start_time_ms=0,
        duration_ms=sign_data.get("duration_ms", 1000),
        end_time_ms=sign_data.get("duration_ms", 1000),
        transition_in_ms=sign_data.get("transition_in_ms", 150),
        transition_out_ms=sign_data.get("transition_out_ms", 150),
        hand_dominance=sign_data.get("hand_dominance", "dominant_only"),
        hand_shape=sign_data.get("hand_shape", "OPEN_FLAT"),
        palm_orientation=sign_data.get("palm_orientation", "INWARD"),
        signing_space=sign_data.get("signing_space", "CHEST_CENTER"),
        movement_type=sign_data.get("movement_type", "HOLD"),
        non_manual_markers=sign_data.get("non_manual_markers", {}),
        is_verified=True,
        joint_targets=sign_data.get("joint_targets"),
        description=sign_data.get("description")
    )

@router.get("/signs/{gloss_id}")
def get_sign_metadata(gloss_id: str):
    sign_data = animation_service.get_sign(gloss_id)
    if not sign_data:
        raise HTTPException(status_code=404, detail=f"Sign '{gloss_id}' not found.")
    return sign_data

@router.get("/assets/manifest")
def get_animation_manifest():
    return animation_service.get_manifest()
