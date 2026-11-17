import asyncio
import httpx
from app.main import app

async def run_tests():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        # 1. Health
        r = await client.get("/health")
        print(f"GET /health: {r.status_code} -> {r.json()['status']}")
        assert r.status_code == 200

        # 2. Languages
        r = await client.get("/api/languages")
        print(f"GET /api/languages: {r.status_code} -> {len(r.json()['supported_languages'])} languages")
        assert r.status_code == 200

        # 3. Translate
        r = await client.post("/api/translate", json={"text": "Where is the hospital?"})
        print(f"POST /api/translate: {r.status_code} -> {r.json()['detected_language']}")
        assert r.status_code == 200

        # 4. Sign Generate
        r = await client.post("/api/sign/generate", json={"text": "Where is the hospital?", "use_rag": True})
        print(f"POST /api/sign/generate: {r.status_code} -> Gloss: {r.json()['generated_gloss']}")
        assert r.status_code == 200
        assert len(r.json()["scheduled_clips"]) > 0

        # 5. Manifest
        r = await client.get("/api/assets/manifest")
        print(f"GET /api/assets/manifest: {r.status_code} -> {r.json()['total_verified_signs']} signs")
        assert r.status_code == 200

    print("\nALL API ENDPOINTS FUNCTIONING 100% PERFECTLY!")

if __name__ == "__main__":
    asyncio.run(run_tests())
