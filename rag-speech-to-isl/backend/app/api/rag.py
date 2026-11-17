from fastapi import APIRouter, HTTPException
from app.models.schemas import RAGQueryRequest, RAGQueryResponse
from app.services.rag_service import rag_service

router = APIRouter(prefix="/api/rag", tags=["RAG Knowledge Base"])

@router.post("/query", response_model=RAGQueryResponse)
def query_rag_index(request: RAGQueryRequest):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query string cannot be empty.")

    results = rag_service.query(
        text=request.query,
        top_k=request.top_k or 3,
        threshold=request.threshold if request.threshold is not None else 0.50
    )

    return RAGQueryResponse(
        query=request.query,
        top_k=request.top_k or 3,
        threshold=request.threshold or 0.50,
        results=results,
        total_index_size=rag_service.total_records
    )

@router.post("/rebuild")
def rebuild_rag_index():
    count = rag_service.rebuild_index()
    return {
        "status": "success",
        "message": f"Successfully re-indexed {count} verified corpus records into FAISS.",
        "total_records": count
    }
