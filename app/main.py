from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.config import API_HOST, API_PORT, DEBUG

# Initialize FastAPI
app = FastAPI(
    title="AI Agent Orchestration System",
    description="Multi-agent LLM system with orchestration, memory management, and real-time streaming",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============ ENDPOINTS ============

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AI Agent Orchestration System",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "environment": "development"}


@app.get("/api/status")
async def api_status():
    """API status endpoint"""
    return {
        "status": "ok",
        "agents": ["search", "coding", "execution"],
        "memory": "ready"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=API_HOST,
        port=API_PORT,
        reload=DEBUG
    )