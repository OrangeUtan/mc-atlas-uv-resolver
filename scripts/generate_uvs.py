import io
import os
from pathlib import Path
from zipfile import ZipFile

import requests
import typer

from scripts import mojang, utils

app = typer.Typer()

ATLASES_ROOT = Path("./build/atlas")
UVS_ROOT = Path("./build/uv")


@app.command()
def cmd_main(minecraft_version: str):
    assets_root = get_assets_root(minecraft_version)

    for category in get_atlas_categories(minecraft_version):
        print(f"Resolving uvs for {category}")

        atlas = get_atlas(minecraft_version, category, "blocks_items")
        out_dir = UVS_ROOT / minecraft_version / category
        textures_dir = assets_root / "minecraft" / "textures"

        generate_uvs(atlas, textures_dir / "item", out_dir / "item.csv")
        generate_uvs(atlas, textures_dir / "block", out_dir / "block.csv")


def download_client_jar(minecraft_version: str):
    client_jar_url = mojang.get_version_downloads(minecraft_version)["client"]["url"]
    response = requests.get(client_jar_url)
    response.raise_for_status()
    return ZipFile(io.BytesIO(response.content), "r")


def get_assets_root(minecraft_version: str):
    assets_root = Path(f".cache/client-{minecraft_version}")
    if assets_root.exists():
        return assets_root / "assets"

    client_jar = download_client_jar(minecraft_version)

    assets_root.parent.mkdir(parents=True, exist_ok=True)
    utils.extract_dirs_from_archive(
        client_jar,
        assets_root,
        ["assets/minecraft/textures/block", "assets/minecraft/textures/item"],
    )

    return assets_root / "assets"


def generate_uvs(atlas: Path, textures_dir: Path, out: Path):
    os.system(
        f"py -m mc_atlas_uv_resolver uv find {atlas} {textures_dir} --posix --table --no-ext --rel {textures_dir} -o {out}"
    )


def get_atlas_categories(minecraft_version: str):
    return map(lambda a: a.name, (ATLASES_ROOT / minecraft_version).iterdir())


def get_atlas(minecraft_version: str, category: str, name: str):
    return ATLASES_ROOT / minecraft_version / category / (name + ".png")


app()
