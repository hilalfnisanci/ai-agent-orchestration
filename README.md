# 🤖 AI Agent Orchestration System

A sophisticated multi-agent AI system built with FastAPI and React that orchestrates specialized agents for web search, code generation, and code execution. Features real-time communication, persistent memory management, and intelligent task routing.

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)
![React](https://img.shields.io/badge/React-18.0+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 🌟 Features

### 🔍 **Search Agent**
- Real-time web search using Serper API
- Returns top 5 relevant results with titles, URLs, and snippets
- Semantic understanding of search queries

### 💻 **Coding Agent**
- Powered by OpenAI GPT-4o-mini
- Generates production-ready Python code
- Includes docstrings, error handling, and PEP 8 compliance
- Automatic syntax validation

### ⚡ **Execution Agent**
- Safe sandboxed code execution
- Timeout protection (30s limit)
- Output capture and error handling
- Security checks for dangerous operations

### 🧠 **Memory Management**
- **Vector Memory**: ChromaDB for semantic search
- **Relational Memory**: SQLite for conversation history
- Persistent storage across sessions
- Intelligent memory recall with relevance scoring

### 🎯 **Smart Orchestration**
- Automatic agent selection based on task type
- Detects whether to search, code, or execute
- Multi-agent task pipelines
- Real-time progress updates via WebSocket

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│         REACT FRONTEND (Vite)               │
│  ├─ Task Input                              │
│  ├─ Real-time Agent Log                     │
│  ├─ Response Display                        │
│  └─ Memory Viewer                           │
└──────────────┬──────────────────────────────┘
               │ HTTP + WebSocket
┌──────────────▼──────────────────────────────┐
│         FASTAPI BACKEND                     │
│  ├─ POST /api/execute-task                  │
│  ├─ GET /api/memory/history                 │
│  ├─ GET /api/memory/{query}                 │
│  └─ WS /ws/agent-stream                     │
└──────────────┬──────────────────────────────┘
               │
    ┌──────────┼──────────┐
    │          │          │
┌───▼────┐ ┌──▼─────┐ ┌──▼────────┐
│SEARCH  │ │CODING  │ │EXECUTION  │
│AGENT   │ │AGENT   │ │AGENT      │
└───┬────┘ └──┬─────┘ └──┬────────┘
    │         │           │
    └─────────┼───────────┘
              │
      ┌───────▼────────┐
      │ MEMORY MANAGER │
      ├─ ChromaDB      │ (vector)
      ├─ SQLite        │ (history)
      └─ Orchestrator  │
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 20.19+ or 22.12+
- OpenAI API Key
- Serper API Key

### 1. Clone Repository

```bash
git clone https://github.com/hilalfnisanci/ai-agent-orchestration.git
cd ai-agent-orchestration
```

### 2. Backend Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
OPENAI_API_KEY=your_openai_api_key_here
SERPER_API_KEY=your_serper_api_key_here
EOF

# Run backend
uvicorn app.main:app --reload
```

Backend will run on `http://localhost:8000`

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run frontend
npm run dev
```

Frontend will run on `http://localhost:5173`

---

## 🎮 Usage Examples

### Example 1: Web Search
```
Input: "Search for latest AI trends"
Agent: SearchAgent
Output: Top 5 relevant articles with links and snippets
```
<img width="576" height="554" alt="Screenshot 2026-01-12 at 17 57 38" src="https://github.com/user-attachments/assets/c8e2912f-b1ec-4fb6-bf99-5126c37429c6" />

### Example 2: Code Generation
```
Input: "Write a Python function to calculate fibonacci numbers"
Agent: CodingAgent
Output: Complete Python code with docstrings and error handling
```
![Untitled design](https://github.com/user-attachments/assets/8c854532-f3d2-464a-9936-8f3bd324da4d)

### Example 3: Code Execution
```
Input: print('Hello from AI Agent!')
Agent: ExecutionAgent
Output: Hello from AI Agent!
```
<img width="571" height="341" alt="Screenshot 2026-01-12 at 18 11 33" src="https://github.com/user-attachments/assets/d9047376-ee02-4a46-a652-abf72d090794" />

### Example 4: Memory Search
```
Navigate to Memory Viewer tab
Search: "fibonacci"
Output: All past tasks related to fibonacci
```
<img width="1158" height="673" alt="Screenshot 2026-01-12 at 18 12 06" src="https://github.com/user-attachments/assets/bc99fcef-6a17-4a36-9276-3d1ebf2b6bfd" />

---

## 📡 API Documentation

### Execute Task
```http
POST /api/execute-task
Content-Type: application/json

{
  "description": "Search for Python tutorials",
  "agent_type": "search"  // optional: auto-detected if not provided
}
```

### Search Memory
```http
GET /api/memory/{query}

Example: GET /api/memory/python
```

### Get Memory History
```http
GET /api/memory/history?limit=50
```

### Clear All Memory
```http
DELETE /api/memory/clear
```

### WebSocket Real-time Updates
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/agent-stream');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Agent update:', data);
};
```

Full API documentation: `http://localhost:8000/docs`

---

## 🗂️ Project Structure

```
ai-agent-orchestration/
├── app/
│   ├── agents/
│   │   ├── base_agent.py          # Abstract base class
│   │   ├── search_agent.py        # Web search (Serper API)
│   │   ├── coding_agent.py        # Code generation (OpenAI)
│   │   └── execution_agent.py     # Code execution (sandbox)
│   ├── memory/
│   │   └── memory_manager.py      # ChromaDB + SQLite
│   ├── orchestrator/
│   │   └── orchestrator.py        # Agent coordination
│   ├── config.py                  # Configuration
│   └── main.py                    # FastAPI app
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── TaskInput.jsx
│   │   │   ├── AgentLog.jsx
│   │   │   ├── ResponseDisplay.jsx
│   │   │   ├── MemoryViewer.jsx
│   │   │   └── Dashboard.jsx
│   │   ├── services/
│   │   │   └── api.js             # API client
│   │   ├── App.jsx
│   │   └── index.css
│   └── package.json
├── data/
│   ├── chroma/                    # Vector embeddings
│   └── memory.db                  # SQLite database
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

---

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key for code generation | Yes |
| `SERPER_API_KEY` | Serper API key for web search | Yes |
| `API_HOST` | Backend host (default: 0.0.0.0) | No |
| `API_PORT` | Backend port (default: 8000) | No |

### Agent Configuration

Edit `app/config.py` to customize:
- Execution timeout limits
- Memory retention policies
- ChromaDB settings
- API endpoints

---

## 🐳 Docker Setup (Optional)

Docker is **optional** for running the backend in a container. Frontend runs separately.

### Prerequisites
- Docker Desktop installed
- `.env` file with API keys in root directory

### Files Already Included
- `Dockerfile` - Backend container configuration
- `docker-compose.yml` - Service orchestration
- `.dockerignore` - Excludes unnecessary files

### Quick Start with Docker
```bash
# 1. Make sure .env file exists with your API keys
cat .env

# 2. Build and start backend
docker-compose up --build

# 3. In another terminal, start frontend
cd frontend
npm run dev
```

### Access Points
- Backend API: `http://localhost:8000`
- API Documentation: `http://localhost:8000/docs`
- Frontend: `http://localhost:5173`

### Docker Commands
```bash
# Start backend (detached mode)
docker-compose up -d

# View logs
docker-compose logs -f

# Stop backend
docker-compose down

# Rebuild after code changes
docker-compose up --build

# Clean everything (including volumes)
docker-compose down -v
```

### Why Docker is Optional

This project works perfectly without Docker. Docker is provided for:
- Consistent development environments
- Easy backend deployment
- Isolation from local Python environment

**For simplest setup**: Just use `uvicorn app.main:app --reload` as shown in Quick Start.

---

## 🧪 Testing

### Manual Testing

1. **Search Agent**: `"Search for Python tutorials"`
2. **Coding Agent**: `"Write a function to sort numbers"`
3. **Execution Agent**: `print("Hello World")`
4. **Memory**: Navigate to Memory Viewer and search past tasks

### API Testing

```bash
# Test search endpoint
curl -X POST http://localhost:8000/api/execute-task \
  -H "Content-Type: application/json" \
  -d '{"description": "Search for AI news"}'

# Test memory endpoint
curl http://localhost:8000/api/memory/history?limit=10
```

---

## 🛡️ Security Features

- **Sandboxed Execution**: Code runs in isolated environment
- **Timeout Protection**: 30-second execution limit
- **Dangerous Operation Blocking**: Prevents file I/O, imports, eval()
- **Input Validation**: Pydantic models for request validation
- **CORS Configuration**: Controlled cross-origin access

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- **FastAPI** - Modern Python web framework
- **React** - Frontend library
- **OpenAI** - GPT-4 for code generation
- **Serper** - Web search API
- **ChromaDB** - Vector database
- **LangChain** - LLM framework utilities

---

## 📧 Contact

**Hilal Nişancı**

- GitHub: [@hilalfnisanci](https://github.com/hilalfnisanci)
- LinkedIn: [Hilal Nişancı](https://www.linkedin.com/in/hilal-nisanci/)

---

## ⭐ Show Your Support

If you find this project useful, please consider giving it a star on GitHub!

---

**Built with ❤️ for AI Agent enthusiasts**
