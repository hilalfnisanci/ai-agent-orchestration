import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
import chromadb
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from app.config import CHROMA_PERSIST_DIR, DATABASE_URL


class MemoryManager:
    """Manage conversation memory with vector search and history"""
    
    def __init__(self):
        # Initialize ChromaDB for vector memory
        self.chroma_client = chromadb.Client()
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        )
        self.vectorstore = Chroma(
            client=self.chroma_client,
            embedding_function=self.embeddings,
            persist_directory=CHROMA_PERSIST_DIR
        )
        
        # Initialize SQLite for history
        self.db_path = DATABASE_URL.replace("sqlite:///", "")
        self._init_db()
    
    def _init_db(self):
        """Initialize SQLite database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL,
                agent_name TEXT NOT NULL,
                result TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                metadata TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    async def store_memory(self, task: str, agent_name: str, result: str, metadata: Dict[str, Any] = None):
        """Store a memory in both vector and relational DB"""
        try:
            # Store in SQLite
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            metadata_json = json.dumps(metadata or {})
            cursor.execute('''
                INSERT INTO memory (task, agent_name, result, metadata)
                VALUES (?, ?, ?, ?)
            ''', (task, agent_name, result, metadata_json))
            
            conn.commit()
            conn.close()
            
            # Store in ChromaDB for semantic search
            doc_text = f"Task: {task}\nAgent: {agent_name}\nResult: {result}"
            self.vectorstore.add_texts(
                texts=[doc_text],
                metadatas=[{
                    "task": task,
                    "agent_name": agent_name,
                    "timestamp": datetime.now().isoformat()
                }]
            )
            
            return {"status": "success", "message": "Memory stored"}
        
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    async def recall_memory(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """Recall relevant memories - simple keyword search"""
        try:
            # Get all documents
            all_results = self.vectorstore.get()
            
            if not all_results or not all_results.get('documents'):
                return []
            
            documents = all_results.get('documents', [])
            metadatas = all_results.get('metadatas', [])
            
            # Filter by keyword
            query_lower = query.lower()
            memories = []
            
            for i, doc in enumerate(documents):
                if query_lower in doc.lower():
                    metadata = metadatas[i] if i < len(metadatas) else {}
                    memories.append({
                        "content": doc,
                        "metadata": metadata,
                        "relevance_score": 0.9,
                        "relevance": "high"
                    })
                    
                    if len(memories) >= k:
                        break
            
            return memories
        except Exception as e:
            print(f"Memory recall error: {str(e)}")
            return []
    
    async def get_conversation_history(self, limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
        """Get conversation history from SQLite"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, task, agent_name, result, timestamp, metadata
                FROM memory
                ORDER BY timestamp DESC
                LIMIT ? OFFSET ?
            ''', (limit, offset))
            
            rows = cursor.fetchall()
            conn.close()
            
            history = []
            for row in rows:
                history.append({
                    "id": row[0],
                    "task": row[1],
                    "agent_name": row[2],
                    "result": row[3],
                    "timestamp": row[4],
                    "metadata": json.loads(row[5]) if row[5] else {}
                })
            
            return history
        
        except Exception as e:
            return [{"error": str(e)}]
    
    async def clear_memory(self):
        """Clear all memory"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('DELETE FROM memory')
            conn.commit()
            conn.close()
            
            return {"status": "success", "message": "Memory cleared"}
        
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    async def get_memory_stats(self) -> Dict[str, Any]:
        """Get memory statistics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT COUNT(*) FROM memory')
            total = cursor.fetchone()[0]
            
            cursor.execute('SELECT DISTINCT agent_name FROM memory')
            agents = [row[0] for row in cursor.fetchall()]
            
            conn.close()
            
            return {
                "total_memories": total,
                "agents_involved": agents,
                "vector_db": "ChromaDB",
                "status": "active"
            }
        
        except Exception as e:
            return {"status": "error", "message": str(e)}
        
    async def get_all_memories(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get all memories from vector store"""
        try:
            # Get all documents from ChromaDB
            results = self.vectorstore.get()
            
            if not results or not results.get('documents'):
                return []
            
            memories = []
            documents = results.get('documents', [])
            metadatas = results.get('metadatas', [])
            
            for i, doc in enumerate(documents[:limit]):
                metadata = metadatas[i] if i < len(metadatas) else {}
                memories.append({
                    'content': doc,
                    'metadata': metadata
                })
            
            return memories
        except Exception as e:
            print(f"Get all memories error: {str(e)}")
            return []