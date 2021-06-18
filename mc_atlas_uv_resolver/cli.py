import os
from pathlib import Path
from typing import Optional

import typer

from mc_atlas_uv_resolver import __version__

from .convert import *


def cb_version(flag: Optional[bool]):
    if flag:
        typer.echo(f"Minecraft texture atlas UVs resolver: Version {__version__}")
        raise typer.Exit()


def cb_main(
    version: Optional[bool] = typer.Option(
        None, "--version", "-v", is_eager=True, callback=cb_version
    )
):
    pass


app = typer.Typer(callback=cb_main, no_args_is_help=True)
app_atlas = typer.Typer(name="atlas", no_args_is_help=True)
app.add_typer(app_atlas)


@app_atlas.command(name="convert", no_args_is_help=True, help="Convert file to texture atlas")
def cmd_atlas(
    source: Path = typer.Argument(..., exists=True, readable=True, dir_okay=False),
    width: Optional[int] = typer.Argument(
        None, help="Atlas width. Automatically derived if omitted"
    ),
    height: Optional[int] = typer.Argument(
        None, help="Atlas height. Automatically derived if omitted"
    ),
    mode: ConversionMode = typer.Option(
        ConversionMode.DEFAULT, "--mode", "-m", case_sensitive=False
    ),
    dest: Optional[Path] = typer.Option(None, "--out", "-o", writable=True, dir_okay=False),
):
    if not dest:
        dest = Path(os.path.dirname(source), f"{source.stem}.png")
    convert_file_to_atlas(source, dest, width, height, mode)
