from fastapi import APIRouter, HTTPException
from app.models.schemas import TranslateRequest, TranslateResponse, LanguagesResponse, LanguageInfo
from app.services.translation_service import translation_service, SUPPORTED_LANGUAGES_CATALOG

router = APIRouter(prefix="/api", tags=["Translation"])
root_router = APIRouter(tags=["Translation"])

@router.get("/languages", response_model=LanguagesResponse)
@root_router.get("/languages", response_model=LanguagesResponse)
def get_supported_languages():
    languages = [LanguageInfo(**item) for item in SUPPORTED_LANGUAGES_CATALOG]
    return LanguagesResponse(
        supported_languages=languages,
        default_language="en"
    )

@router.post("/translate", response_model=TranslateResponse)
def translate_and_normalize(request: TranslateRequest):
    try:
        return translation_service.normalize_and_analyze(
            text=request.text,
            source_language=request.source_language
        )
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Language normalization error: {str(e)}")
