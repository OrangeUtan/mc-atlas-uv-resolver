from pathlib import Path

import cv2
from PIL.Image import Image

__all__ = ["find_texture_uvs_in_atlas", "find_all_texture_uvs_in_atlas"]


def find_texture_uvs_in_atlas(texture: Image, atlas: Image) -> tuple[int, int]:
    _, _, location, _ = cv2.minMaxLoc(cv2.matchTemplate(atlas, texture, cv2.TM_SQDIFF_NORMED))
    return location


def find_all_texture_uvs_in_atlas(textures: list[Path], atlas_path: Path):
    atlas = cv2.imread(str(atlas_path))
    for path in textures:
        texture: Image = cv2.imread(str(path))
        u, v = find_texture_uvs_in_atlas(atlas, texture)
        yield path, u, v
