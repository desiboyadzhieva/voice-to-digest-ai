# voice-to-digest-ai

A local "NotebookLM" for voice recordings. Feed it audio files, then ask questions across all your transcripts — entirely offline, nothing leaves your machine.

## How it works

1. **Transcribe** — Drop an audio file in; faster-whisper converts speech to text and saves it as a dated `.txt` file.
2. **Index** — LlamaIndex reads all transcripts and builds a local vector search index using Ollama embeddings.
3. **Ask** — Ask any question in plain English; the app retrieves the most relevant transcript chunks and uses Ollama (llama3) to write a grounded answer.

## Prerequisites

### 1. Python 3.10 or newer
Download from https://python.org if needed.

> **Note:** If `pip install faster-whisper` fails on Python 3.13+, create your virtual environment with Python 3.12 instead:
> ```
> py -3.12 -m venv venv
> ```

### 2. Ollama (local LLM runtime)
Download from https://ollama.com and start it. Then pull the two required models:

```
ollama pull llama3
ollama pull nomic-embed-text
```

## Setup

```bash
# Clone the repo
git clone https://github.com/desiboyadzhieva/voice-to-digest-ai.git
cd voice-to-digest-ai

# Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Transcribe an audio file

```bash
python main.py transcribe path/to/meeting.mp3
python main.py transcribe path/to/meeting.mp3 --topic weekly_sync
```

The transcript is saved to `transcripts/YYYY-MM-DD_<topic>.txt`.

### Index all transcripts

Run this after adding new transcripts:

```bash
python main.py index
```

### Ask a question

```bash
python main.py ask "What did we decide about the API redesign?"
python main.py ask "Who mentioned the budget?" --top-k 5
```

The answer is printed along with the source files it was drawn from.

### Optional: web UI

```bash
python ui/gradio_app.py
```

Open http://127.0.0.1:7860 in your browser for a point-and-click interface with tabs for Transcribe, Index, and Ask.

## Supported audio formats

mp3, wav, m4a, ogg, flac, webm, and most other formats that ffmpeg supports.

## Configuration

Edit `voice_digest/config.py` to change:

| Setting | Default | Notes |
|---|---|---|
| `WHISPER_MODEL` | `base` | `tiny` is faster; `small`/`medium`/`large-v3` are more accurate |
| `WHISPER_DEVICE` | `cpu` | Use `cuda` if you have an NVIDIA GPU |
| `OLLAMA_LLM_MODEL` | `llama3` | Any model you have pulled with `ollama pull` |
| `OLLAMA_EMBED_MODEL` | `nomic-embed-text` | Must match what you pulled |

## Project structure

```
voice-to-digest-ai/
├── voice_digest/        Core library (transcriber, indexer, asker)
├── cli/                 Command-line interface (Typer)
├── ui/                  Optional Gradio web UI
├── transcripts/         Where your .txt transcripts are stored
├── index_store/         Persisted vector index (rebuilt with `vtd index`)
└── main.py              Entry point
```
