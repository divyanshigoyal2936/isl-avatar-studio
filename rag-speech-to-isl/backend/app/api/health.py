from fastapi import APIRouter
from app.core.config import settings
from app.models.schemas import HealthResponse
from app.services.rag_service import rag_service
from app.services.animation_service import animation_service

router = APIRouter(tags=["Health"])

@router.get("/health", response_model=HealthResponse)
@router.get("/api/health", response_model=HealthResponse)
def get_health():
    return HealthResponse(
        status="healthy",
        app_name=settings.APP_NAME,
        version=settings.APP_VERSION,
        models={
            "embedding_model": settings.EMBEDDING_MODEL_NAME,
            "embedding_dimension": rag_service.embedder.dimension,
            "stt_provider": settings.STT_PROVIDER
        },
        rag_index={
            "status": "ready" if rag_service.total_records > 0 else "empty",
            "total_indexed_exemplars": rag_service.total_records,
            "similarity_metric": "cosine_inner_product",
            "top_k_default": settings.FAISS_TOP_K
        },
        animation_library={
            "status": "ready",
            "total_verified_signs": len(animation_service.manifest),
            "rig_standard": "ISLRTC_Humanoid_Rig"
        },
        database="connected"
    )
