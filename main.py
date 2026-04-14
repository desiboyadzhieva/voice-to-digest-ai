import typer
from pathlib import Path

from voice_digest.transcriber import transcribe as _transcribe
from voice_digest.indexer import build_index
from voice_digest.asker import ask as _ask

app = typer.Typer(
    name="vtd",
    help=(
        "voice-to-digest-ai\n\n"
        "Transcribe audio recordings, index the transcripts, and ask questions "
        "across all of them — entirely offline."
    ),
)


@app.command()
def transcribe(
    audio_file: str = typer.Argument(..., help="Path to the audio file (mp3, wav, m4a, …)"),
    topic: str = typer.Option(None, "--topic", "-t", help="Optional topic label for the filename."),
) -> None:
    """Transcribe an audio file and save the transcript."""
    path = Path(audio_file)
    if not path.exists():
        typer.echo(f"Error: file not found — {audio_file}", err=True)
        raise typer.Exit(1)
    typer.echo(f"Transcribing {path.name} …")
    out = _transcribe(str(path), topic=topic)
    typer.echo(f"Transcript saved: {out}")


@app.command()
def index() -> None:
    """Index all transcripts in transcripts/ for question-answering."""
    typer.echo("Building index from transcripts/ …")
    try:
        build_index()
        typer.echo("Index built and saved to index_store/")
    except ValueError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(1)


@app.command()
def ask(
    question: str = typer.Argument(..., help="The question to ask."),
    top_k: int = typer.Option(3, "--top-k", "-k", help="Number of transcript chunks to use as context."),
) -> None:
    """Ask a question over all indexed transcripts."""
    result = _ask(question, top_k=top_k)
    typer.echo(f"\nAnswer:\n{result['answer']}\n")
    if result["sources"]:
        typer.echo("Sources:")
        for s in result["sources"]:
            typer.echo(f"  - {s['file']}  (relevance score: {s['score']})")


if __name__ == "__main__":
    app()
