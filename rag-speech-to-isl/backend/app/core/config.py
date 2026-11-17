import os
from pathlib import Path
from pydantic_settings import BaseSettings

# Base directories
BACKEND_DIR = Path(__file__).resolve().parent.parent.parent
PROJECT_ROOT = BACKEND_DIR.parent
DATA_DIR = PROJECT_ROOT / "data"

class Settings(BaseSettings):
    APP_NAME: str = "ISL Avatar Studio"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    API_PREFIX: str = "/api"
    
    # Storage / DB
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{str(PROJECT_ROOT).replace(chr(92), '/')}/isl_avatar.db")
    
    # RAG & Embedding settings
    EMBEDDING_MODEL_NAME: str = "all-MiniLM-L6-v2"
    FAISS_INDEX_PATH: str = str(DATA_DIR / "faiss_index.bin")
    FAISS_METADATA_PATH: str = str(DATA_DIR / "faiss_metadata.json")
    FAISS_TOP_K: int = 3
    FAISS_SIMILARITY_THRESHOLD: float = 0.50
    
    # Datasets
    CORPUS_DIR: str = str(DATA_DIR / "corpus")
    ANIMATION_MANIFEST_PATH: str = str(DATA_DIR / "animation_manifest.json")
    
    # Speech to text
    STT_PROVIDER: str = os.getenv("STT_PROVIDER", "whisper")
    STT_MAX_AUDIO_SIZE_BYTES: int = 15 * 1024 * 1024  # 15 MB
    STT_MAX_AUDIO_DURATION_SEC: int = 60
    
    # CORS
    ALLOWED_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "*"
    ]
    
    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()
