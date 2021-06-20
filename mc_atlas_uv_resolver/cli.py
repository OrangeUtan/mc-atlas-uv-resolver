import csv
import os
from pathlib import Path
from typing import Iterable, Optional, TextIO

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
    as_table: bool = typer.Option(False, "--table", "-t", help="Output as table"),
    dest: Optional[Path] = typer.Option(None, "--out", "-o", writable=True, dir_okay=False),
    posix: bool = typer.Option(False, "--posix", "-p", help="Format paths as posix"),
    relative_to: Optional[Path] = typer.Option(None, "--rel", exists=True),
    remove_extension: bool = typer.Option(
        False, "--no-ext", help="Remove file extension from paths"
    ),
):
    if dest:
        dest.parent.mkdir(parents=True, exist_ok=True)

    # Resolve texture uvs
    flattened_textures = utils.flatten_paths(textures)
    texture_uvs = uvs.find_all_texture_uvs_in_atlas(
        list(filter(lambda t: t.suffix == ".png", flattened_textures)), atlas
    )
    formatted_texture_uvs = format_texture_uvs(texture_uvs, posix, relative_to, remove_extension)

    # Output texture uvs
    show_progress = as_table or dest
    if show_progress:
        with typer.progressbar(
            formatted_texture_uvs,
            length=len(flattened_textures),
            label="Resolving UVs",
            item_show_func=lambda i: str(i[0]) if i else "",
        ) as progress:
            output_texture_uvs(progress, as_table, dest)
    else:
        output_texture_uvs(formatted_texture_uvs, as_table, dest)


def format_texture_uvs(
    uvs: Iterable[tuple[Path, int, int]], posix: bool, relative_to: Optional[Path], remove_ext: bool
) -> Iterable[tuple[Path, int, int]]:
    if relative_to:
        uvs = map(lambda e: (e[0].relative_to(relative_to), *e[1:]), uvs)

    if remove_ext:
        uvs = map(lambda e: (e[0].with_suffix(""), *e[1:]), uvs)

    if posix:
        uvs = map(lambda e: (e[0].as_posix(), *e[1:]), uvs)

    return uvs


def output_texture_uvs(uvs: Iterable[tuple[Path, int, int]], as_table: bool, dest: Optional[Path]):
    if dest:
        newline = "" if as_table else None
        with dest.open("w", newline=newline) as f:
            write_texture_uvs(uvs, f, as_table)
    else:
        print_texture_uvs(uvs, as_table)


def print_texture_uvs(uvs: Iterable[tuple[Path, int, int]], as_table: bool):
    if as_table:
        table = PrettyTable(["texture", "x", "y"])
        table.align["texture"] = "l"
        for path, u, v in uvs:
            table.add_row([path, u, v])
        print(table)
        return
    else:
        for path, u, v in uvs:
            print(path, u, v)


def write_texture_uvs(uvs: Iterable[tuple[Path, int, int]], file: TextIO, as_table: bool):
    if as_table:
        writer = csv.writer(file, dialect="excel")
        for row in uvs:
            writer.writerow(row)
    else:
        for path, u, v in uvs:
            file.write(f"{path} {u} {v}\n")
