import os
from dotenv import load_dotenv

load_dotenv()

# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Search API
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY", "")

# Environment
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
DEBUG = os.getenv("DEBUG", "True") == "True"

# Database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/memory.db")

# ChromaDB
CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./data/chroma")

# API Settings
API_PORT = int(os.getenv("API_PORT", 8000))
API_HOST = os.getenv("API_HOST", "0.0.0.0")

# Agent Settings
MAX_TOKENS = 2000
TEMPERATURE = 0.7