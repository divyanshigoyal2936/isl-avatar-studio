import datetime
import logging
from typing import Generator
from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, Session

from app.core.config import settings

logger = logging.getLogger("Database")

# Determine engine parameters
connect_args = {}
if settings.DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False

engine = create_engine(settings.DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class CorpusRecordModel(Base):
    __tablename__ = "corpus_records"

    id = Column(String(64), primary_key=True, index=True)
    dataset = Column(String(32), nullable=False)
    split = Column(String(16), default="train")
    language = Column(String(16), nullable=False)
    source_text = Column(Text, nullable=False)
    normalized_english = Column(Text, nullable=False)
    gloss_sequence = Column(Text, nullable=False)  # JSON-encoded array
    domain = Column(String(64))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class AnimationClipModel(Base):
    __tablename__ = "animation_clips"

    gloss_id = Column(String(64), primary_key=True, index=True)
    hand_dominance = Column(String(32))
    hand_shape = Column(String(32))
    palm_orientation = Column(String(32))
    signing_space = Column(String(64))
    duration_ms = Column(Integer)
    validation_status = Column(String(32), default="VERIFIED")
    description = Column(Text)

class ConsentedSessionRecord(Base):
    __tablename__ = "consented_sessions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(64), index=True)
    input_text = Column(Text, nullable=False)
    detected_language = Column(String(16))
    generated_gloss = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    user_consent = Column(Boolean, default=False)

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables initialized successfully.")
    except Exception as e:
        logger.error(f"Error initializing database tables: {e}")
