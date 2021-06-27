import os
from pathlib import Path

import typer
import yaml

from scripts.Settings import Settings

app = typer.Typer()


@app.command()
def cmd_main(minecraft_version: str):

    for category in get_atlas_categories(minecraft_version):
        print(f"Resolving uvs for {category}")

        atlas = get_atlas(minecraft_version, category, "blocks_items")
        out_dir = settings.uvs_root / minecraft_version / category
        textures_dir = (
            settings.get_version_assets_root(minecraft_version) / "minecraft" / "textures"
        )

        generate_uvs(atlas, textures_dir / "item", out_dir / "item.csv")
        generate_uvs(atlas, textures_dir / "block", out_dir / "block.csv")


def generate_uvs(atlas: Path, textures_dir: Path, out: Path):
    os.system(
        f"py -m mc_atlas_uv_resolver uv find {atlas} {textures_dir} --posix --table --no-ext --rel {textures_dir} -o {out}"
    )


def get_atlas_categories(minecraft_version: str):
    return map(lambda a: a.name, (settings.atlases_root / minecraft_version).iterdir())


def get_atlas(minecraft_version: str, category: str, name: str):
    return settings.atlases_root / minecraft_version / category / (name + ".png")


def get_settings(path: Path):
    with path.open("r") as f:
        return yaml.safe_load(f)


settings = Settings.load(Path("scripts/settings.yml"))
app()
