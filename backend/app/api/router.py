from fastapi import APIRouter
from app.api.health import router as health_router
from app.api.transcribe import router as transcribe_router
from app.api.translate import router as translate_router, root_router as translate_root_router
from app.api.sign import router as sign_router
from app.api.rag import router as rag_router
from app.api.evaluate import router as evaluate_router

api_router = APIRouter()

api_router.include_router(health_router)
api_router.include_router(transcribe_router)
api_router.include_router(translate_router)
api_router.include_router(translate_root_router)
api_router.include_router(sign_router)
api_router.include_router(rag_router)
api_router.include_router(evaluate_router)
