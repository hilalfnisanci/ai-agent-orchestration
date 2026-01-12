from typing import Dict, Any, List
import asyncio
from app.agents import SearchAgent, CodingAgent, ExecutionAgent, AgentResponse
from app.memory.memory_manager import MemoryManager


class AgentOrchestrator:
    """Orchestrate multiple agents to complete complex tasks"""
    
    def __init__(self):
        self.agents = {
            "search": SearchAgent(),
            "coding": CodingAgent(),
            "execution": ExecutionAgent()
        }
        self.memory = MemoryManager()
        self.execution_history = []
    
    async def execute_task(self, task: str, agent_type: str = None) -> Dict[str, Any]:
        """
        Execute a task using appropriate agent(s)
        
        Args:
            task: Task description
            agent_type: Specific agent to use (search/coding/execution)
                       If None, auto-select based on task
        
        Returns:
            Orchestration result with agent responses
        """
        try:
            # Auto-detect agent type if not specified
            if not agent_type:
                agent_type = await self._detect_agent_type(task)
            
            # Get appropriate agent
            if agent_type not in self.agents:
                return {
                    "status": "error",
                    "message": f"Unknown agent type: {agent_type}",
                    "available_agents": list(self.agents.keys())
                }
            
            agent = self.agents[agent_type]
            
            # Execute task
            response = await agent.execute(task)
            
            # Store in memory
            await self.memory.store_memory(
                task=task,
                agent_name=response.agent_name,
                result=response.result,
                metadata=response.metadata
            )
            
            # Record execution
            execution_record = {
                "task": task,
                "agent": agent_type,
                "response": response.dict(),
                "status": response.status
            }
            self.execution_history.append(execution_record)
            
            return {
                "status": "success",
                "orchestration": {
                    "task": task,
                    "agent_type": agent_type,
                    "agent_response": response.dict()
                }
            }
        
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "task": task
            }
    
    async def execute_multi_agent_task(self, task: str) -> Dict[str, Any]:
        """
        Execute a complex task using multiple agents in sequence
        
        Example: "Search for Python async patterns, then generate code, then execute it"
        """
        try:
            results = []
            context = task
            
            # Step 1: Search
            search_result = await self.agents["search"].execute(context)
            results.append(search_result)
            
            # Step 2: Generate code based on search results
            coding_task = f"Generate Python code based on: {search_result.result}"
            coding_result = await self.agents["coding"].execute(coding_task)
            results.append(coding_result)
            
            # Step 3: Execute the generated code (if safe)
            if coding_result.status == "success":
                exec_result = await self.agents["execution"].execute(coding_result.result)
                results.append(exec_result)
            
            # Store each step in memory
            for result in results:
                await self.memory.store_memory(
                    task=task,
                    agent_name=result.agent_name,
                    result=result.result,
                    metadata=result.metadata
                )
            
            return {
                "status": "success",
                "task": task,
                "steps": [r.dict() for r in results],
                "final_result": results[-1].result if results else None
            }
        
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "task": task
            }
    
    async def _detect_agent_type(self, task: str) -> str:
        """Auto-detect which agent to use based on task description"""
        task_lower = task.lower()
        task_stripped = task.strip()
        
        # Priority 1: Explicit search keywords (highest priority for search)
        search_keywords = ["search for", "find information", "look up", "research about", 
                        "what is", "tell me about", "information about"]
        if any(keyword in task_lower for keyword in search_keywords):
            return "search"
        
        # Priority 2: Check if it's actual Python code (not just keywords in sentences)
        # Must have Python syntax patterns AND be short (likely code snippet)
        code_patterns = ["print(", "def ", "class ", "import ", "return ", "if __name__"]
        has_code_pattern = any(pattern in task for pattern in code_patterns)
        is_short = len(task_stripped.split()) < 30  # Less than 30 words
        
        if has_code_pattern and is_short:
            return "execution"
        
        # Priority 3: Execution requests (with verbs)
        execution_keywords = ["run this", "execute this", "test this code", "run the code"]
        if any(keyword in task_lower for keyword in execution_keywords):
            return "execution"
        
        # Priority 4: Code generation requests
        coding_keywords = ["write code", "write a function", "write a class", "generate code",
                        "create a function", "implement a", "code to", "python function",
                        "algorithm for", "write python"]
        if any(keyword in task_lower for keyword in coding_keywords):
            return "coding"
        
        # Priority 5: Question-based detection
        if task_stripped.endswith("?"):
            return "search"
        
        # Priority 6: Default based on structure
        # Multi-line code without explanation → execution
        if "\n" in task and has_code_pattern:
            return "execution"
        
        # Single line with code syntax → execution
        if "(" in task and ")" in task and any(p in task for p in ["print", "len", "range", "sum"]):
            return "execution"
        
        # Default: if unsure, use search (safest option)
        return "search"
    
    async def get_agent_status(self) -> Dict[str, Any]:
        """Get status of all agents"""
        memory_stats = await self.memory.get_memory_stats()
        
        return {
            "status": "active",
            "agents": list(self.agents.keys()),
            "memory": memory_stats,
            "execution_history_count": len(self.execution_history),
            "timestamp": "now"
        }
    
    async def recall_context(self, query: str) -> Dict[str, Any]:
        """Recall relevant memories for context"""
        memories = await self.memory.recall_memory(query, k=5)
        
        return {
            "query": query,
            "relevant_memories": memories,
            "count": len(memories)
        }
    
    async def get_execution_history(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get execution history"""
        return self.execution_history[-limit:]
    
    async def clear_memory(self) -> Dict[str, Any]:
        """Clear all memory"""
        return await self.memory.clear_memory()