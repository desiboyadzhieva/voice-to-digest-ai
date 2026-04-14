"""
Optional web UI for voice-to-digest-ai.

Run with:
    python ui/gradio_app.py

Then open http://127.0.0.1:7860 in your browser.

Requires Ollama to be running locally and the index to be built first
(python main.py index).
"""

import gradio as gr

from voice_digest.transcriber import transcribe
from voice_digest.indexer import build_index
from voice_digest.asker import ask


def _transcribe_ui(audio_path: str, topic: str) -> str:
    if not audio_path:
        return "Please enter a path to an audio file."
    out = transcribe(audio_path, topic or None)
    return f"Saved: {out}"


def _index_ui() -> str:
    try:
        build_index()
        return "Index rebuilt successfully."
    except ValueError as exc:
        return str(exc)


def _ask_ui(question: str, top_k: int) -> tuple[str, str]:
    if not question.strip():
        return "Please enter a question.", ""
    result = ask(question, top_k=int(top_k))
    sources_str = "\n".join(
        f"- {s['file']}  (score: {s['score']})" for s in result["sources"]
    )
    return result["answer"], sources_str or "No sources found."


with gr.Blocks(title="voice-to-digest-ai") as demo:
    gr.Markdown("# voice-to-digest-ai\nTranscribe recordings. Ask questions. All offline.")

    with gr.Tab("1 — Transcribe"):
        gr.Markdown("Provide the path to an audio file. It will be transcribed and saved to `transcripts/`.")
        audio_in  = gr.Textbox(label="Audio file path", placeholder="C:/path/to/meeting.mp3")
        topic_in  = gr.Textbox(label="Topic label (optional)", placeholder="weekly_sync")
        t_btn     = gr.Button("Transcribe", variant="primary")
        t_out     = gr.Textbox(label="Result", interactive=False)
        t_btn.click(_transcribe_ui, inputs=[audio_in, topic_in], outputs=t_out)

    with gr.Tab("2 — Index"):
        gr.Markdown("Rebuild the search index after adding new transcripts.")
        i_btn = gr.Button("Rebuild Index", variant="primary")
        i_out = gr.Textbox(label="Status", interactive=False)
        i_btn.click(_index_ui, outputs=i_out)

    with gr.Tab("3 — Ask"):
        gr.Markdown("Ask any question. The answer is drawn from your transcript library.")
        q_in  = gr.Textbox(label="Your question", placeholder="What did we decide about the launch date?")
        k_in  = gr.Slider(1, 10, value=3, step=1, label="Sources to retrieve (top-K)")
        a_btn = gr.Button("Ask", variant="primary")
        a_out = gr.Textbox(label="Answer", interactive=False, lines=6)
        s_out = gr.Textbox(label="Sources used", interactive=False, lines=4)
        a_btn.click(_ask_ui, inputs=[q_in, k_in], outputs=[a_out, s_out])


if __name__ == "__main__":
    demo.launch()
