# ISL Knowledge Base & Animation Assets

## Overview
This directory contains the curated datasets, schemas, and animation manifests supporting the RAG-Augmented Speech-to-ISL translation system.

## Datasets
1. **ISL-CSLTR (Continuous Sign Language Translation and Recognition in Indian Sign Language)**
   - Curated conversational and emergency sentence-gloss pairs.
   - Preserves authentic ISL grammar (SOV word order, initial time markers, sentence-final interrogatives, and non-manual facial grammatical markers).
   - Provenance: Open academic research dataset (ISLRTC reference alignment).

2. **CISLR (Continuous Indian Sign Language Recognition)**
   - Multilingual domain-specific corpora across Indian languages (Hindi, English, Tamil, Telugu, Bengali, Marathi, etc.).
   - Contains navigation, medical, educational, and daily communication pairs.

3. **Held-Out Benchmark Evaluation Set (`benchmark_eval.json`)**
   - Strictly reserved for evaluation and generalization testing.
   - **Never inserted into the FAISS retrieval index** to prevent data contamination and circular evaluation.

## Animation Manifest (`animation_manifest.json`)
The animation library defines verified ISL sign tokens with:
- Hand dominance (dominant only, bimanual symmetric, bimanual asymmetric).
- Hand shape (Open flat, Fist, Index point, Claw, Pinch, V-shape, Cup, Thumbs up).
- Palm orientation and signing space.
- Movement trajectory and timing (duration, ease-in, ease-out).
- Non-manual markers (eyebrow position, head movements, mouthing).
- Skeletal joint rotation targets for humanoid rigs.

## Adding New Verified Signs
To add a new verified sign:
1. Validate against `data/schemas/animation_manifest_schema.json`.
2. Add the unique gloss identifier (e.g. `NEW_SIGN`).
3. Record joint rotation keyframes, duration, and facial marker annotations.
4. Run validation tests: `python -m unittest backend.tests.test_animation`.
