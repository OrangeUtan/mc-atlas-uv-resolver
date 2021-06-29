from functools import cache

import requests


@cache
def download_version_manifest() -> dict:
    response = requests.get("https://launchermeta.mojang.com/mc/game/version_manifest.json")
    response.raise_for_status()
    return response.json()


def get_version_downloads(minecraft_version: str) -> dict:
    manifest = download_version_manifest()
    version_info = next(
        version for version in manifest["versions"] if version["id"] == minecraft_version
    )

    response = requests.get(version_info["url"])
    response.raise_for_status()
    return response.json()["downloads"]
