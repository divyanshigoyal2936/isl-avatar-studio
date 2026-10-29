# RAG-Augmented Speech-to-Indian Sign Language (ISL) Human Avatar Generator

An accessible web application where users can speak or type in an Indian language (Hindi, English, Tamil, Telugu, Bengali, Marathi, Gujarati, etc.) and receive visual Indian Sign Language (ISL) explanations performed by a realistic 3D human avatar.

---

## Key Features

1. **Multilingual Speech & Text Input**:
   - Web Audio API browser microphone capture with live waveform and recording status.
   - Audio file upload (WAV, WebM, MP3, M4A).
   - Audio preprocessing & transcription via Distil-Whisper / Acoustic Analyzer.
   - User transcript review & correction before translation.

2. **ISL-Aware Language Pipeline**:
   - Syntactic translation respecting authentic ISL grammar (SOV word order, time markers upfront, sentence-final question and negation markers).
   - Omission of non-meaning copulas and function words.

3. **RAG Knowledge Base (FAISS + MiniLM)**:
   - Dense sentence embeddings using `sentence-transformers/all-MiniLM-L6-v2`.
   - FAISS vector database indexed with authentic ISL-CSLTR and CISLR sentence-gloss pairs.
   - Generalization test split strictly isolated to prevent data leakage.

4. **3D Rigged Humanoid Avatar**:
   - Real-time WebGL rendering via Three.js.
   - Expressive humanoid rig with articulated spine, shoulders, arms, wrists, fingers, and animated eyebrows for non-manual grammatical markers.
   - Playback controls: Play, Pause, Restart, Step-by-Step, Speed (0.5x to 1.5x), Loop Sign, and Mirrored Learning View.

5. **Transparency & Benchmarking**:
   - Linguistic explanation mode for each translation.
   - Transparent fallback alerts when a sign lacks certified motion data.
   - Quantitative benchmark evaluation module (Recall@k, Exact Match, Token F1, BLEU-1, verified coverage, latency).

---

## Quick Start (Run Locally)

### Prerequisites
- Python 3.10+ (tested on Python 3.13)
- Node.js 18+ (optional, for frontend dev mode)

### 1. Launch the Backend & Web Application
Double-click `run_backend.bat` or run in PowerShell:
```powershell
Set-Location backend
$env:PYTHONPATH = (Get-Location).Path
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### 2. Open in Your Browser
Visit:https://isl-avatar-studio.onrender.com


---

## Running Automated Tests

Run the full automated test suite (30 unit & integration tests):
```powershell
Set-Location backend
python -m unittest discover tests
```

---

## Project Structure
```
rag-speech-to-isl/
├── backend/
│   ├── app/
│   │   ├── api/             # FastAPI REST endpoints
│   │   ├── core/            # Config & settings
│   │   ├── database/        # Database & SQLAlchemy models
│   │   ├── models/          # Typed Pydantic schemas
│   │   └── services/        # STT, translation, RAG, gloss, animation, evaluation
│   ├── tests/               # 30 automated unit & integration tests
│   └── requirements.txt
├── data/
│   ├── corpus/              # ISL-CSLTR, CISLR, benchmark eval split
│   ├── schemas/             # JSON schemas for corpus & animation manifests
│   ├── animation_manifest.json
│   ├── faiss_index.bin      # Pre-built FAISS vector index
│   └── faiss_metadata.json
├── frontend/
│   ├── public/index.html    # Integrated 3D avatar client served by FastAPI
│   ├── src/                 # React + TypeScript + Tailwind source code
│   └── package.json
├── docs/                    # Architecture and ISL grammar documentation
├── scripts/                 # Utility scripts (index rebuild, evaluation)
├── run_backend.bat          # 1-click Windows launcher
└── docker-compose.yml
```
