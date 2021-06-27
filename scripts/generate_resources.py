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
    archive_path = out_root / minecraft_version / "uvs.zip"
    archive_path.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(archive_path, "w") as archive:
        add_dir_to_archive(archive, settings.uvs_root / minecraft_version)


def generate_atlas_resources(minecraft_version: str):
    archive_path = out_root / minecraft_version / "atlases.zip"
    archive_path.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(archive_path, "w") as archive:
        add_dir_to_archive(archive, settings.atlases_root / minecraft_version)


def get_uv_categories(minecraft_version: str):
    return map(lambda a: a.name, (settings.uvs_root / minecraft_version).iterdir())


def add_dir_to_archive(archive: ZipFile, dir: Path):
    for folder, _, filenames in os.walk(dir):
        for file in filenames:
            path = Path(folder, file)
            archive.write(path, path.relative_to(dir))


settings = Settings.load(Path("scripts/settings.yml"))
app()
