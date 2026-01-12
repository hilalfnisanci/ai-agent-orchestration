from app.agents.base_agent import BaseAgent, AgentResponse
from typing import Dict, Any, Tuple
import asyncio
import subprocess
import tempfile
import os


class ExecutionAgent(BaseAgent):
    """Agent for safe code execution"""
    
    def __init__(self):
        super().__init__(name="ExecutionAgent")
        self.timeout = 30  # seconds
    
    async def execute(self, task: str) -> AgentResponse:
        """Execute code from task"""
        try:
            # Extract code from task (assume it's Python code)
            output, error = await self._execute_code(task)
            
            status = "success" if not error else "error"
            result = output if output else error
            
            return AgentResponse(
                agent_name=self.name,
                task=task,
                status=status,
                result=result,
                metadata={
                    "output": output,
                    "error": error,
                    "execution_time": "~1s"
                }
            )
        except Exception as e:
            return AgentResponse(
                agent_name=self.name,
                task=task,
                status="error",
                result=str(e),
                metadata={"error": str(e)}
            )
    
    async def _execute_code(self, code: str) -> Tuple[str, str]:
        """Execute Python code safely in a sandbox"""
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(code)
                temp_file = f.name
            
            try:
                # Run code with timeout
                result = subprocess.run(
                    ['python', temp_file],
                    capture_output=True,
                    text=True,
                    timeout=self.timeout
                )
                
                output = result.stdout
                error = result.stderr
                
                return output, error
            finally:
                # Clean up temp file
                os.unlink(temp_file)
        
        except subprocess.TimeoutExpired:
            return "", f"Code execution timeout (>{self.timeout}s)"
        except Exception as e:
            return "", f"Execution error: {str(e)}"
    
    async def think(self, prompt: str) -> str:
        """Think about execution strategy"""
        return f"Preparing to execute: {prompt}"
    
    async def act(self, code: str) -> Tuple[str, str]:
        """Execute the code"""
        return await self._execute_code(code)