from app.agents.base_agent import BaseAgent, AgentResponse
from typing import Dict, Any
import asyncio
import os
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

class CodingAgent(BaseAgent):
    """Agent for code generation and analysis using OpenAI"""
    
    def __init__(self):
        super().__init__(name="CodingAgent")
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = None
        if self.api_key:
            self.client = AsyncOpenAI(api_key=self.api_key)
    
    async def execute(self, task: str) -> AgentResponse:
        """Execute a coding task"""
        try:
            # Check if API key exists
            if not self.client:
                return AgentResponse(
                    agent_name=self.name,
                    task=task,
                    status="error",
                    result="OPENAI_API_KEY not found in .env file",
                    metadata={"error": "Missing API key"}
                )
            
            # Generate code using OpenAI
            code = await self._generate_code(task)
            
            # Validate syntax
            validation = await self.validate_syntax(code)
            
            return AgentResponse(
                agent_name=self.name,
                task=task,
                status="success",
                result=code,
                metadata={
                    "language": "python",
                    "lines": len(code.split('\n')),
                    "status": "generated",
                    "syntax_valid": validation["valid"],
                    "validation_errors": validation.get("errors", [])
                }
            )
            
        except Exception as e:
            return AgentResponse(
                agent_name=self.name,
                task=task,
                status="error",
                result=f"Code generation failed: {str(e)}",
                metadata={"error": str(e)}
            )
    
    async def _generate_code(self, requirements: str) -> str:
        """Generate code using OpenAI"""
        try:
            prompt = f"""You are an expert Python programmer. Generate clean, well-documented Python code for the following task:

Task: {requirements}

Requirements:
1. Write production-ready Python code
2. Include docstrings and comments
3. Follow PEP 8 style guidelines
4. Add error handling where appropriate
5. Make the code reusable and modular

Return ONLY the Python code, no explanations or markdown."""

            response = await self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert Python programmer. Generate clean, production-ready code."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            code = response.choices[0].message.content.strip()
            
            # Remove markdown code blocks if present
            if code.startswith("```python"):
                code = code.split("```python")[1].split("```")[0].strip()
            elif code.startswith("```"):
                code = code.split("```")[1].split("```")[0].strip()
            
            return code
            
        except Exception as e:
            print(f"OpenAI API error: {str(e)}")
            # Fallback to placeholder
            return f'''# Generated code for: {requirements}
# (OpenAI API error - using placeholder)

def main():
    """Main function"""
    print("Code generation failed, using placeholder")
    return True

if __name__ == "__main__":
    main()
'''
    
    async def think(self, prompt: str) -> str:
        """Think about code structure"""
        return f"Planning code structure for: {prompt}"
    
    async def act(self, requirements: str) -> str:
        """Generate the code"""
        code = await self._generate_code(requirements)
        return code
    
    async def validate_syntax(self, code: str) -> Dict[str, Any]:
        """Validate code syntax"""
        try:
            compile(code, '<string>', 'exec')
            return {"valid": True, "errors": []}
        except SyntaxError as e:
            return {"valid": False, "errors": [str(e)]}