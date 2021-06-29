from pathlib import Path
from zipfile import ZipFile


def extract_dirs_from_archive(archive: ZipFile, dest: Path, dirs: list[str]):
    for file in filter(lambda f: any(map(lambda d: f.startswith(d), dirs)), archive.namelist()):
        archive.extract(file, dest)
