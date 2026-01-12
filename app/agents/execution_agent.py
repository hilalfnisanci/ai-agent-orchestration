from app.agents.base_agent import BaseAgent, AgentResponse
from typing import Dict, Any, Tuple
import asyncio
import subprocess
import tempfile
import os
import time

class ExecutionAgent(BaseAgent):
    """Agent for safe code execution in sandbox"""
    
    def __init__(self):
        super().__init__(name="ExecutionAgent")
        self.timeout = 30  # seconds
        self.max_output_size = 10000  # characters
    
    async def execute(self, task: str) -> AgentResponse:
        """Execute code from task"""
        try:
            # Validate code before execution
            if not self._is_safe_code(task):
                return AgentResponse(
                    agent_name=self.name,
                    task=task,
                    status="error",
                    result="Code contains potentially unsafe operations",
                    metadata={"error": "Unsafe code detected"}
                )
            
            # Execute code and measure time
            start_time = time.time()
            output, error = await self._execute_code(task)
            execution_time = round(time.time() - start_time, 2)
            
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
                    "execution_time": f"{execution_time}s"
                }
            )
            
        except Exception as e:
            return AgentResponse(
                agent_name=self.name,
                task=task,
                status="error",
                result=f"Execution failed: {str(e)}",
                metadata={"error": str(e)}
            )
    
    def _is_safe_code(self, code: str) -> bool:
        """Basic safety check for code"""
        # Dangerous operations to block
        dangerous_patterns = [
            'import os',
            'import sys',
            'import subprocess',
            'eval(',
            'exec(',
            '__import__',
            'open(',
            'file(',
            'input(',
            'raw_input(',
        ]
        
        code_lower = code.lower()
        for pattern in dangerous_patterns:
            if pattern.lower() in code_lower:
                return False
        
        return True
    
    async def _execute_code(self, code: str) -> Tuple[str, str]:
        """Execute Python code safely in a sandbox"""
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(code)
                temp_file = f.name
            
            try:
                # Run code with timeout
                result = await asyncio.create_subprocess_exec(
                    'python3', temp_file,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                
                try:
                    stdout, stderr = await asyncio.wait_for(
                        result.communicate(),
                        timeout=self.timeout
                    )
                    
                    output = stdout.decode('utf-8', errors='ignore')
                    error = stderr.decode('utf-8', errors='ignore')
                    
                    # Truncate if too long
                    if len(output) > self.max_output_size:
                        output = output[:self.max_output_size] + "\n... (output truncated)"
                    
                    if len(error) > self.max_output_size:
                        error = error[:self.max_output_size] + "\n... (error truncated)"
                    
                    return output, error
                    
                except asyncio.TimeoutError:
                    result.kill()
                    return "", f"Code execution timeout (>{self.timeout}s)"
                    
            finally:
                # Clean up temp file
                if os.path.exists(temp_file):
                    os.unlink(temp_file)
                    
        except Exception as e:
            return "", f"Execution error: {str(e)}"
    
    async def think(self, prompt: str) -> str:
        """Think about execution strategy"""
        return f"Preparing to execute: {prompt}"
    
    async def act(self, code: str) -> Tuple[str, str]:
        """Execute the code"""
        return await self._execute_code(code)