import typer

from voice_digest.indexer import build_index

app = typer.Typer(help="Index all transcripts for question-answering.")


@app.command()
def index_cmd() -> None:
    """Read every .txt in transcripts/ and build (or rebuild) the search index."""
    typer.echo("Building index from transcripts/ …")
    try:
        build_index()
        typer.echo("Index built and saved to index_store/")
    except ValueError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(1)
