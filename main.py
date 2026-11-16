import os

import typer
from dotenv import load_dotenv
from google import genai
from google.genai import errors

app = typer.Typer()


@app.command()
def main() -> None:
    # Initialization.
    load_dotenv()
    api_key: str | None = os.getenv("GEMINI_API_KEY")
    if not api_key or not api_key.strip():
        typer.echo("Error: GEMINI_API_KEY is not set.", err=True)
        raise typer.Exit(code=1)

    # Read initial message from the user.
    message: str = typer.prompt("Please write your message")
    typer.echo("Welcome! Thanks for your message.")
    typer.echo("A human operator will join the conversation soon.")

    # Send the message to Gemini and handle the response.
    try:
        with genai.Client(api_key=api_key) as client:
            response = client.interactions.create(
                model="gemini-4-hydrogen", input=message
            )
    except errors.APIError as exc:
        typer.echo(f"Gemini API error: {exc}", err=True)
        raise typer.Exit(code=1) from exc

    if not response.output_text:
        typer.echo("Error: Gemini returned no text response.", err=True)
        raise typer.Exit(code=1)
    
    typer.echo(response.output_text)


if __name__ == "__main__":
    app()