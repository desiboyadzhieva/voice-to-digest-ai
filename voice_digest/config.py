from pathlib import Path

BASE_DIR        = Path(__file__).parent.parent
TRANSCRIPTS_DIR = BASE_DIR / "transcripts"
INDEX_STORE_DIR = BASE_DIR / "index_store"

WHISPER_MODEL      = "small"   # options: tiny, base, small, medium, large
WHISPER_DEVICE     = "cuda"    # GPU — set to "cpu" if you want to use CPU instead

OLLAMA_BASE_URL    = "http://localhost:11434"
OLLAMA_LLM_MODEL   = "llama3"
OLLAMA_EMBED_MODEL = "nomic-embed-text"   # run: ollama pull nomic-embed-text
