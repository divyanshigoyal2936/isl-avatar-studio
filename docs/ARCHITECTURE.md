# System Architecture: RAG-Augmented Speech-to-ISL Avatar Generator

## High-Level Architecture

The system converts speech and text in Indian languages (Hindi, English, Tamil, Telugu, Bengali, Marathi, etc.) into authentic 3D Indian Sign Language (ISL) animations performed by an expressive humanoid avatar.

```
[ Multilingual User Input (Voice / Text) ]
                   │
                   ▼
       [ Stage 1: Transcription ]
        (Distil-Whisper / Audio Analyzer)
                   │
                   ▼
     [ Stage 2: Language Normalization ]
     (Unicode script detector & Intent Parser)
                   │
                   ▼
       [ Stage 3: RAG Retrieval ]
  (MiniLM Embeddings + FAISS Vector Index)
                   │
                   ▼
     [ Stage 4: ISL Gloss Generation ]
   (Authentic SOV & Topic-Comment Grammar)
                   │
                   ▼
      [ Stage 5: Sign Clip Mapping ]
   (ISLRTC / CISLR Verified Motion Manifest)
                   │
                   ▼
    [ Stage 6: 3D Skeletal Scheduling ]
(Joint Rotations, Easing, Non-Manual Facial Markers)
                   │
                   ▼
   [ Stage 7: WebGL 3D Avatar Rendering ]
(Three.js Humanoid Viewer with Playback Controls)
```

## Core Modules
1. **Frontend**:
   - Modern WebGL 3D humanoid avatar with full skeletal hierarchy (spine, neck, head, shoulders, arms, hands, individual finger joints, and animated eyebrows for facial grammar).
   - Audio recording with real-time feedback and review/correction input box.
   - Playback controls: Play, Pause, Restart, Step Forward/Back, Speed Scaling (0.5x to 1.5x), Loop Sign, and Mirrored Learning View.
2. **Backend**:
   - FastAPI server with typed Pydantic models.
   - MiniLM sentence embeddings + FAISS vector search (`IndexFlatIP`).
   - Authentic ISL grammar transformations:
     - Time markers first (`[TIME] TODAY`)
     - Subject-Object-Verb ordering
     - Negation and Question markers placed at the end with corresponding facial grammar (`EYEBROWS_RAISED`, `HEAD_SHAKE`).
     - Copulas and non-meaning function words omitted.
   - Comprehensive test suite covering all services, models, and endpoints.
