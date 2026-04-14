from pathlib import Path

BASE_DIR        = Path(__file__).parent.parent
TRANSCRIPTS_DIR = BASE_DIR / "transcripts"
INDEX_STORE_DIR = BASE_DIR / "index_store"

WHISPER_MODEL      = "large-v3"  # options: tiny, base, small, medium, large-v2, large-v3
WHISPER_LANGUAGE   = "bg"      # Bulgarian — set to None to auto-detect

import torch
WHISPER_DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

OLLAMA_BASE_URL    = "http://localhost:11434"
OLLAMA_LLM_MODEL   = "llama3"
OLLAMA_EMBED_MODEL = "nomic-embed-text"   # run: ollama pull nomic-embed-text
