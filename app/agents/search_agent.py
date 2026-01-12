from app.agents.base_agent import BaseAgent, AgentResponse
from typing import List, Dict, Any
import asyncio
import os
import aiohttp
from dotenv import load_dotenv

load_dotenv()

class SearchAgent(BaseAgent):
    """Agent for web search and information retrieval using Serper API"""
    
    def __init__(self):
        super().__init__(name="SearchAgent")
        self.api_key = os.getenv("SERPER_API_KEY")
        self.search_url = "https://google.serper.dev/search"
        
    async def execute(self, task: str) -> AgentResponse:
        """Execute a search task"""
        try:
            # Check if API key exists
            if not self.api_key:
                return AgentResponse(
                    agent_name=self.name,
                    task=task,
                    status="error",
                    result="SERPER_API_KEY not found in .env file",
                    metadata={"error": "Missing API key"}
                )
            
            # Perform real search
            results = await self._search(task)
            
            if not results:
                return AgentResponse(
                    agent_name=self.name,
                    task=task,
                    status="success",
                    result="No results found for your query",
                    metadata={"results_count": 0, "results": []}
                )
            
            return AgentResponse(
                agent_name=self.name,
                task=task,
                status="success",
                result=f"Found {len(results)} results for: {task}",
                metadata={"results_count": len(results), "results": results}
            )
            
        except Exception as e:
            return AgentResponse(
                agent_name=self.name,
                task=task,
                status="error",
                result=f"Search failed: {str(e)}",
                metadata={"error": str(e)}
            )
    
    async def _search(self, query: str) -> List[Dict[str, Any]]:
        """Perform real search using Serper API"""
        try:
            headers = {
                'X-API-KEY': self.api_key,
                'Content-Type': 'application/json'
            }
            
            payload = {
                'q': query,
                'num': 5  # Get top 5 results
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.search_url,
                    json=payload,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    if response.status != 200:
                        print(f"Serper API error: {response.status}")
                        return []
                    
                    data = await response.json()
                    
                    # Parse organic results
                    results = []
                    organic = data.get('organic', [])
                    
                    for item in organic[:5]:  # Limit to 5 results
                        results.append({
                            'title': item.get('title', 'No title'),
                            'url': item.get('link', '#'),
                            'snippet': item.get('snippet', 'No description available')
                        })
                    
                    return results
                    
        except asyncio.TimeoutError:
            print("Search request timed out")
            return []
        except Exception as e:
            print(f"Search error: {str(e)}")
            return []
    
    async def think(self, prompt: str) -> str:
        """Think about search strategy"""
        return f"Analyzing search query: {prompt}"
    
    async def act(self, query: str) -> str:
        """Perform the search"""
        results = await self._search(query)
        return f"Search completed with {len(results)} results"