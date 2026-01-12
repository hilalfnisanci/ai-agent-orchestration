from abc import ABC, abstractmethod
from typing import Any, Dict, List
from pydantic import BaseModel


class AgentResponse(BaseModel):
    """Agent response model"""
    agent_name: str
    task: str
    status: str  # "success" or "error"
    result: str
    metadata: Dict[str, Any] = {}


class BaseAgent(ABC):
    """Base class for all agents"""
    
    def __init__(self, name: str):
        self.name = name
        self.tools = []
    
    @abstractmethod
    async def execute(self, task: str) -> AgentResponse:
        """Execute task - must be implemented by subclasses"""
        pass
    
    def add_tool(self, tool):
        """Add a tool to the agent"""
        self.tools.append(tool)
    
    async def think(self, prompt: str) -> str:
        """Think about a prompt - to be implemented"""
        pass
    
    async def act(self, action: str) -> str:
        """Act on a decision - to be implemented"""
        pass