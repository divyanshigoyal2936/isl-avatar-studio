import os
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from app.services.rag_service import rag_service

if __name__ == "__main__":
    print("Building FAISS index from verified ISL corpus...")
    count = rag_service.rebuild_index()
    print(f"FAISS index built and saved successfully with {count} exemplars.")
