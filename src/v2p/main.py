import typer
import pyperclip
from typing import Optional
from pathlib import Path

app = typer.Typer()

@app.command()
def generate(
    prompt: str = typer.Argument(..., help="The informal prompt to transform"),
    copy: bool = typer.Option(True, "--copy", help="Copy output to clipboard"),
    file: Optional[Path] = typer.Option(None, "--file", help="Save output to file")
):
    """Transform an informal prompt into a structured technical prompt."""
    
    from .llm import get_structured_prompt

    typer.echo("Generating prompt...")
    try:
        structured_prompt = get_structured_prompt(prompt)
    except Exception as e:
        typer.echo(f"Error: Failed to connect to Gemini API. ({e})", err=True)
        raise typer.Exit(code=1)

    if copy:
        pyperclip.copy(structured_prompt)
        typer.echo("Structured prompt copied to clipboard!")
        
    if file:
        file.write_text(structured_prompt)
        typer.echo(f"Structured prompt saved to {file}")
        
    typer.echo(f"\nResult:\n{structured_prompt}")

if __name__ == "__main__":
    app()
