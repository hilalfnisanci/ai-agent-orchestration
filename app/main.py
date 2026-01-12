from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from app.config import API_HOST, API_PORT, DEBUG
from app.orchestrator import AgentOrchestrator

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

# Initialize orchestrator
orchestrator = AgentOrchestrator()

# ============ MODELS ============

class TaskRequest(BaseModel):
    """Task execution request"""
    description: str 
    agent_type: Optional[str] = None


class MemoryQuery(BaseModel):
    """Memory recall query"""
    query: str
    limit: Optional[int] = 5


# ============ ENDPOINTS ============

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AI Agent Orchestration System",
        "version": "1.0.0",
        "docs": "/docs",
        "agents": ["search", "coding", "execution"]
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "environment": "development"}


@app.get("/api/status")
async def api_status():
    """API status endpoint"""
    return await orchestrator.get_agent_status()


# ============ TASK EXECUTION ENDPOINTS ============

@app.post("/api/execute-task")
async def execute_task(request: TaskRequest):
    """
    Execute a task using agents
    
    Args:
        task: Task description
        agent_type: Optional agent type (search/coding/execution)
    """
    result = await orchestrator.execute_task(
        task=request.description,  # description kullan
        agent_type=request.agent_type
    )
    return result


@app.post("/api/execute-multi-agent")
async def execute_multi_agent(request: TaskRequest):
    """
    Execute a complex task using multiple agents in sequence
    """
    result = await orchestrator.execute_multi_agent_task(request.task)
    return result


# ============ MEMORY ENDPOINTS ============

@app.post("/api/memory/recall")
async def recall_memory(request: MemoryQuery):
    """
    Recall relevant memories using semantic search
    """
    result = await orchestrator.recall_context(request.query)
    return result


@app.get("/api/memory/history")
async def get_memory_history(limit: int = 50, offset: int = 0):
    """
    Get conversation history
    """
    memories = await orchestrator.memory.get_conversation_history(limit, offset)
    return {"history": memories, "count": len(memories)}


@app.delete("/api/memory/clear")
async def clear_memory():
    """
    Clear all memory (use with caution!)
    """
    result = await orchestrator.clear_memory()
    return result


@app.get("/api/memory/stats")
async def get_memory_stats():
    """
    Get memory statistics
    """
    stats = await orchestrator.memory.get_memory_stats()
    return stats


# ============ HISTORY ENDPOINTS ============

@app.get("/api/execution-history")
async def get_execution_history(limit: int = 20):
    """
    Get execution history
    """
    history = await orchestrator.get_execution_history(limit)
    return {"history": history, "count": len(history)}


# ============ WEBSOCKET ENDPOINT ============

@app.websocket("/ws/agent-stream")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time agent updates
    """
    await websocket.accept()
    try:
        while True:
            # Receive task from client
            data = await websocket.receive_json()
            task = data.get("task")
            
            if not task:
                await websocket.send_json({"error": "No task provided"})
                continue
            
            # Send thinking notification
            await websocket.send_json({
                "event": "agent_thinking",
                "message": "Processing task..."
            })
            
            # Execute task
            result = await orchestrator.execute_task(task)
            
            # Send result
            await websocket.send_json({
                "event": "agent_complete",
                "data": result
            })
    
    except Exception as e:
        try:
            await websocket.send_json({"error": str(e)})
        except:
            pass
    finally:
        try:
            await websocket.close()
        except:
            pass  # Already closed


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=API_HOST,
        port=API_PORT,
        reload=DEBUG
    )