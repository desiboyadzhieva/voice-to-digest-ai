import typer
from pathlib import Path

from voice_digest.transcriber import transcribe

app = typer.Typer(help="Transcribe an audio file and save the transcript.")


@app.command()
def transcribe_cmd(
    audio_file: str = typer.Argument(..., help="Path to the audio file (mp3, wav, m4a, …)"),
    topic: str = typer.Option(
        None, "--topic", "-t",
        help="Optional topic label used in the output filename."
    ),
) -> None:
    """Transcribe AUDIO_FILE and save the result to transcripts/."""
    path = Path(audio_file)
    if not path.exists():
        typer.echo(f"Error: file not found — {audio_file}", err=True)
        raise typer.Exit(1)

    typer.echo(f"Transcribing {path.name} …")
    out = transcribe(str(path), topic=topic)
    typer.echo(f"Transcript saved: {out}")
