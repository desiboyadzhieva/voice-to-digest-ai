from voice_digest.indexer import load_index


def ask(question: str, top_k: int = 3) -> dict:
    """
    Ask a natural-language question over all indexed transcripts.

    Parameters
    ----------
    question : str
        The question to answer.
    top_k : int
        Number of transcript chunks to retrieve for context.

    Returns
    -------
    dict with keys:
        "answer"  : str   — the LLM's answer
        "sources" : list  — [{"file": str, "score": float}, …]
    """
    index = load_index()
    query_engine = index.as_query_engine(similarity_top_k=top_k)
    response = query_engine.query(question)

    sources = []
    if response.source_nodes:
        for node in response.source_nodes:
            fname = node.metadata.get("file_name", "unknown")
            score = round(node.score or 0.0, 3)
            sources.append({"file": fname, "score": score})

    return {
        "answer": str(response),
        "sources": sources,
    }
