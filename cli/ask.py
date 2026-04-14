import typer

from voice_digest.asker import ask

app = typer.Typer(help="Ask a question over all indexed transcripts.")


@app.command()
def ask_cmd(
    question: str = typer.Argument(..., help="The question to ask."),
    top_k: int = typer.Option(
        3, "--top-k", "-k",
        help="Number of transcript chunks to use as context (default: 3)."
    ),
) -> None:
    """Ask QUESTION and get an answer sourced from your transcripts."""
    result = ask(question, top_k=top_k)
    typer.echo(f"\nAnswer:\n{result['answer']}\n")
    if result["sources"]:
        typer.echo("Sources:")
        for s in result["sources"]:
            typer.echo(f"  - {s['file']}  (relevance score: {s['score']})")
