import os
from pathlib import Path
from typing import Optional

import typer
from prettytable import PrettyTable

from mc_atlas_uv_resolver import __version__

from . import utils, uvs
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
app_uvs = typer.Typer(name="uvs", no_args_is_help=True)
app.add_typer(app_atlas)
app.add_typer(app_uvs)


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


@app_uvs.command(name="find", no_args_is_help=True, help="Find texture uvs on a texture atlas")
def cmd_find_texture_uvs_on_atlas(
    atlas: Path = typer.Argument(..., exists=True, readable=True, dir_okay=False),
    textures: list[Path] = typer.Argument(..., exists=True, readable=True),
    print_table: bool = typer.Option(False, "--table"),
    dest: Optional[Path] = typer.Option(None, "--out", "-o", writable=True, dir_okay=False),
):
    flattened_textures = utils.flatten_paths(textures)
    texture_uvs = uvs.find_all_texture_uvs_in_atlas(
        list(filter(lambda t: t.suffix == ".png", flattened_textures)), atlas
    )

    if dest:
        with dest.open("w") as f:
            with typer.progressbar(
                texture_uvs,
                length=len(flattened_textures),
                label="Resolving UVs",
                item_show_func=lambda i: str(i[0].name) if i else "",
            ) as progess:
                for path, u, v in progess:
                    f.write(f"{path} {u}, {v}\n")
    elif print_table:
        table = PrettyTable(["texture", "x", "y"])
        table.align["texture"] = "l"
        with typer.progressbar(
            texture_uvs,
            length=len(flattened_textures),
            label="Resolving UVs",
            item_show_func=lambda i: str(i[0].name) if i else "",
        ) as progress:
            for path, u, v in progress:
                table.add_row([path, u, v])
        print(table)
    else:
        for path, u, v in texture_uvs:
            print(path, u, v)
