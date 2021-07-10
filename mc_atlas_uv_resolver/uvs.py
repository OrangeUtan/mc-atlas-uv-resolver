from pathlib import Path

import cv2
from numpy import ndarray

__all__ = ["find_texture_uvs_in_atlas", "find_all_texture_uvs_in_atlas"]


def find_texture_uvs_in_atlas(texture: ndarray, atlas: ndarray) -> tuple[int, int]:
    _, _, location, _ = cv2.minMaxLoc(cv2.matchTemplate(atlas, texture, cv2.TM_SQDIFF_NORMED))
    return location


def find_all_texture_uvs_in_atlas(textures: list[Path], atlas_path: Path):
    atlas: ndarray = cv2.imread(str(atlas_path), cv2.IMREAD_UNCHANGED)
    for path in textures:
        texture: ndarray = cv2.imread(str(path), cv2.IMREAD_UNCHANGED)
        height, width, channels = texture.shape

        # Add alpha channel if missing
        if channels != 4:
            texture = cv2.cvtColor(texture, cv2.COLOR_RGB2RGBA)

        # Crop animated textures
        if width != height:
            texture = texture[0:width]
            u, v = find_texture_uvs_in_atlas(texture, atlas)
            yield path, u, v
        else:
            u, v = find_texture_uvs_in_atlas(texture, atlas)
            yield path, u, v
