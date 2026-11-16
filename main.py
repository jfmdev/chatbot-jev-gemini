import typer

app = typer.Typer()


@app.command()
def main() -> None:
    typer.prompt("Please write your message")
    typer.echo("Welcome! Thanks for your message.")
    typer.echo("A human operator will join the conversation soon.")


if __name__ == "__main__":
    app()