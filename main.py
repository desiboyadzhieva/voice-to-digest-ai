import typer

from cli.transcribe import app as transcribe_app
from cli.index import app as index_app
from cli.ask import app as ask_app

app = typer.Typer(
    name="vtd",
    help=(
        "voice-to-digest-ai\n\n"
        "Transcribe audio recordings, index the transcripts, and ask questions "
        "across all of them — entirely offline."
    ),
)

app.add_typer(transcribe_app, name="transcribe")
app.add_typer(index_app,      name="index")
app.add_typer(ask_app,        name="ask")

if __name__ == "__main__":
    app()
