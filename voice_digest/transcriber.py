import whisper
from datetime import date
from pathlib import Path
import re

from voice_digest.config import TRANSCRIPTS_DIR, WHISPER_MODEL, WHISPER_DEVICE


def _slugify(text: str, max_words: int = 5) -> str:
    """Turn arbitrary text into a safe filename fragment."""
    words = re.sub(r"[^a-zA-Z0-9\s]", "", text).split()[:max_words]
    return "_".join(w.lower() for w in words) if words else "recording"


def transcribe(audio_path: str, topic: str | None = None) -> Path:
    """
    Transcribe an audio file with openai-whisper and save the result to
    transcripts/<date>_<topic>.txt.

    Parameters
    ----------
    audio_path : str
        Path to the audio file (mp3, wav, m4a, ogg, flac, …).
    topic : str | None
        Optional label for the filename. If omitted, the first words of
        the transcript are used.

    Returns
    -------
    Path
        Full path to the saved transcript file.
    """
    model = whisper.load_model(WHISPER_MODEL, device=WHISPER_DEVICE)
    result = model.transcribe(audio_path)
    full_text = result["text"].strip()

    if not topic:
        topic = _slugify(full_text, max_words=5)
    else:
        topic = _slugify(topic)

    TRANSCRIPTS_DIR.mkdir(exist_ok=True)
    filename = f"{date.today().isoformat()}_{topic}.txt"
    out_path = TRANSCRIPTS_DIR / filename
    out_path.write_text(full_text, encoding="utf-8")
    return out_path
