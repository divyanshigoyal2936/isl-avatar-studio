import os
from pathlib import Path
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse

from app.core.config import settings
from app.database.db import init_db
from app.api.router import api_router

# Initialize Database
init_db()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="RAG-Augmented Speech-to-Indian Sign Language (ISL) Human Avatar Generator with 3D animation, authentic grammar parsing, and FAISS vector retrieval.",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API routes
app.include_router(api_router)

# Frontend directories
FRONTEND_DIR = Path(__file__).resolve().parent.parent.parent / "frontend"
DIST_DIR = FRONTEND_DIR / "dist"
PUBLIC_DIR = FRONTEND_DIR / "public"

if DIST_DIR.exists():
    app.mount("/assets", StaticFiles(directory=str(DIST_DIR / "assets")), name="assets")

if PUBLIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(PUBLIC_DIR)), name="static")

@app.get("/avatar.glb")
async def serve_avatar_glb():
    glb_path = PUBLIC_DIR / "avatar.glb"
    if glb_path.exists():
        return FileResponse(glb_path, media_type="model/gltf-binary")
    return HTMLResponse("Not Found", status_code=404)

@app.get("/", response_class=HTMLResponse)
async def serve_index(request: Request):
    """
    Serves the primary web client. If a production dist index exists, serves it;
    otherwise serves the rich standalone accessible interface from public/index.html.
    """
    dist_index = DIST_DIR / "index.html"
    if dist_index.exists():
        return FileResponse(dist_index)
    
    public_index = PUBLIC_DIR / "index.html"
    if public_index.exists():
        return FileResponse(public_index)

    return HTMLResponse(
        """
        <!DOCTYPE html>
        <html>
        <head><title>ISL Avatar Studio</title></head>
        <body style="font-family:sans-serif; text-align:center; padding:50px; background:#0f172a; color:#f8fafc;">
            <h1>ISL Avatar Studio Backend Active</h1>
            <p>API documentation available at <a href="/docs" style="color:#38bdf8;">/docs</a></p>
        </body>
        </html>
        """
    )

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        await websocket.send_json({"type": "status", "message": "ISL Avatar Studio Connected"})
        while True:
            data = await websocket.receive_text()
            await websocket.send_json({"type": "pong", "payload": data})
    except (WebSocketDisconnect, Exception):
        pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
