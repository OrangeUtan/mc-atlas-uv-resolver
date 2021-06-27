import os
from pathlib import Path
from zipfile import ZipFile

import typer

from scripts.Settings import Settings

app = typer.Typer()

out_root = Path("dist").absolute()


@app.command()
def cmd_main(minecraft_version: str):
    generate_uv_resources(minecraft_version)
    generate_atlas_resources(minecraft_version)


def generate_uv_resources(minecraft_version: str):
    for category in get_uv_categories(minecraft_version):
        archive_path = out_root / minecraft_version / f"uvs_{category}.zip"
        archive_path.parent.mkdir(parents=True, exist_ok=True)
        with ZipFile(archive_path, "w") as archive:
            for path in (settings.uvs_root / minecraft_version / category).iterdir():
                archive.write(path, path.name)


def generate_atlas_resources(minecraft_version: str):
    archive_path = out_root / minecraft_version / "atlases.zip"
    archive_path.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(archive_path, "w") as archive:
        for folder, _, filenames in os.walk(settings.atlases_root / minecraft_version):
            for file in filenames:
                path = Path(folder, file)
                archive.write(path, path.relative_to(settings.atlases_root / minecraft_version))


def get_uv_categories(minecraft_version: str):
    return map(lambda a: a.name, (settings.uvs_root / minecraft_version).iterdir())


settings = Settings.load(Path("scripts/settings.yml"))
app()
