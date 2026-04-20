"""
Interactome-AI Backend — FastAPI Application Entry Point.

This is the main server. It:
1. Creates the FastAPI app with metadata
2. Configures CORS so the Next.js frontend can call us
3. Mounts all API routers (/api/predict, /api/drugs, /api/graph)
4. Exposes a health check endpoint
5. Serves the API docs at /docs (Swagger UI)

Run with: uvicorn app.main:app --reload --port 8000
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import predict, drugs, graph

# ── Create FastAPI Application ────────────────────────────────
app = FastAPI(
    title="Interactome-AI",
    description=(
        "A predictive framework for higher-order adverse drug reactions "
        "in multi-medication regimens. Powered by Graph Neural Networks."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── CORS Middleware ───────────────────────────────────────────
# Allow the Next.js frontend (port 3000) to call our API (port 8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",    # Next.js dev server
        "http://127.0.0.1:3000",
        "http://frontend:3000",     # Docker service name
        "*",                        # Allow all for development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Mount API Routers ────────────────────────────────────────
app.include_router(predict.router)
app.include_router(drugs.router)
app.include_router(graph.router)


# ── Health Check ─────────────────────────────────────────────
@app.get("/health", tags=["System"])
async def health_check():
    """Health check endpoint for monitoring and Docker health checks."""
    return {
        "status": "healthy",
        "service": "Interactome-AI Backend",
        "version": "1.0.0",
    }


@app.get("/", tags=["System"])
async def root():
    """Root endpoint with API info."""
    return {
        "name": "Interactome-AI API",
        "description": "Drug interaction prediction powered by Graph Neural Networks",
        "docs": "/docs",
        "endpoints": {
            "predict": "POST /api/predict",
            "drug_search": "GET /api/drugs/search?q=<query>",
            "drug_detail": "GET /api/drugs/<name>",
            "graph": "GET /api/graph?drugs=<drug1,drug2,...>",
            "pdf_report": "POST /api/predict/pdf",
        },
    }
