from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
from app.models.schemas import TranscribeResponse
from app.services.stt_service import stt_service

router = APIRouter(prefix="/api", tags=["Speech"])

@router.post("/transcribe", response_model=TranscribeResponse)
async def transcribe_audio(
    file: UploadFile = File(...),
    language: Optional[str] = Form("auto")
):
    # Validate content type
    allowed_types = ["audio/", "video/webm", "application/octet-stream"]
    content_type = file.content_type or ""
    if not any(t in content_type for t in allowed_types) and not file.filename.endswith((".wav", ".mp3", ".webm", ".m4a", ".ogg")):
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported audio format: '{content_type}'. Please upload WAV, WebM, MP3, or M4A audio."
        )

    try:
        audio_bytes = await file.read()
        transcript, detected_lang, confidence, duration = stt_service.transcribe(
            audio_bytes=audio_bytes,
            filename=file.filename or "recording.webm",
            language_hint=language
        )
        return TranscribeResponse(
            transcript=transcript,
            detected_language=detected_lang,
            confidence=confidence,
            duration_seconds=duration,
            provider="Distil-Whisper-Acoustic-Analyzer"
        )
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Speech transcription pipeline error: {str(e)}")
