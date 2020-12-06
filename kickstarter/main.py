from pathlib import Path

import typer

from .data_extraction.preprocess import process

app = typer.Typer()


@app.command()
def run():
    typer.echo("Hello World!")


@app.command()
def preprocess(
    input_dir: Path = typer.Argument(...), output_dir: Path = typer.Argument(...)
):
    process(str(input_dir), str(output_dir))
