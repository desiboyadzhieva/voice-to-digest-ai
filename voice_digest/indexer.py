from llama_index.core import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    StorageContext,
    load_index_from_storage,
    Settings,
)
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding

from voice_digest.config import (
    TRANSCRIPTS_DIR,
    INDEX_STORE_DIR,
    OLLAMA_BASE_URL,
    OLLAMA_LLM_MODEL,
    OLLAMA_EMBED_MODEL,
)


def _configure_settings() -> None:
    """Point LlamaIndex at the local Ollama instance."""
    Settings.llm = Ollama(
        model=OLLAMA_LLM_MODEL,
        base_url=OLLAMA_BASE_URL,
        request_timeout=120.0,
    )
    Settings.embed_model = OllamaEmbedding(
        model_name=OLLAMA_EMBED_MODEL,
        base_url=OLLAMA_BASE_URL,
    )


def build_index() -> VectorStoreIndex:
    """
    Read every .txt file in transcripts/, build a vector index, and
    persist it to index_store/ for future queries.

    Raises
    ------
    ValueError
        If no transcript files are found.
    """
    _configure_settings()
    docs = SimpleDirectoryReader(
        str(TRANSCRIPTS_DIR), required_exts=[".txt"]
    ).load_data()
    if not docs:
        raise ValueError(
            f"No .txt files found in {TRANSCRIPTS_DIR}. "
            "Run 'python main.py transcribe <file>' first."
        )
    index = VectorStoreIndex.from_documents(docs, show_progress=True)
    INDEX_STORE_DIR.mkdir(exist_ok=True)
    index.storage_context.persist(persist_dir=str(INDEX_STORE_DIR))
    return index


def load_index() -> VectorStoreIndex:
    """Load a previously built index from index_store/."""
    _configure_settings()
    storage = StorageContext.from_defaults(persist_dir=str(INDEX_STORE_DIR))
    return load_index_from_storage(storage)
