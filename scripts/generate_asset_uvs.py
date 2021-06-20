import os
from pathlib import Path

import typer

app = typer.Typer()


@app.command(no_args_is_help=True)
def cmd_main(
    atlases_root: Path = typer.Argument(...),
    textures_root: Path = typer.Argument(...),
):
    version = atlases_root.parts[-1]

    for category in map(lambda a: a.name, atlases_root.iterdir()):
        print(f"Resoling {category}")

        atlas = atlases_root / category / "blocks_items.png"
        out_root = Path(f"build/uv/{version}/{category}")

        resolve_uvs(atlas, textures_root, "item", out_root)
        resolve_uvs(atlas, textures_root, "block", out_root)


def resolve_uvs(atlas: Path, textures_root: Path, texture_category: str, out_root: Path):
    out = Path(out_root / (texture_category + ".csv"))
    textures = textures_root / texture_category

    os.system(
        f"py -m mc_atlas_uv_resolver uv find {atlas} {textures} --posix --table --no-ext --rel {textures} -o {out}"
    )


app()
