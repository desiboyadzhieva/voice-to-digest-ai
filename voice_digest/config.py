from pathlib import Path

BASE_DIR        = Path(__file__).parent.parent
TRANSCRIPTS_DIR = BASE_DIR / "transcripts"
INDEX_STORE_DIR = BASE_DIR / "index_store"

WHISPER_MODEL      = "base"    # options: tiny, base, small, medium, large-v3
WHISPER_DEVICE     = "cpu"     # use "cuda" if you have an NVIDIA GPU
WHISPER_COMPUTE    = "int8"    # keeps RAM low on CPU; use "float16" on GPU

OLLAMA_BASE_URL    = "http://localhost:11434"
OLLAMA_LLM_MODEL   = "llama3"
OLLAMA_EMBED_MODEL = "nomic-embed-text"   # run: ollama pull nomic-embed-text
