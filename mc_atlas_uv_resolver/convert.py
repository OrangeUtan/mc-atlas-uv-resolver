import logging
import math
from enum import Enum
from pathlib import Path
from typing import Optional

import PIL.Image as Image

__all__ = ["convert_file_to_atlas", "ConversionMode"]
logger = logging.getLogger(__name__)


class ConversionMode(str, Enum):
    BINARY = ("bin",)
    DEFAULT = BINARY


def derive_atlas_dimensions(num_pixels: int, width: Optional[int], height: Optional[int]):
    if not width and not height:
        width = height = int(math.sqrt(num_pixels))
    elif not width:
        width = int(num_pixels / height)
    else:
        height = int(num_pixels / width)

    if width % 2 != 0 or height % 2 != 0:
        raise ValueError("Couldn't derive atlas size")

    return (width, height)


def convert_file_to_atlas(
    source: Path,
    dest: Path,
    width: Optional[int] = None,
    height: Optional[int] = None,
    mode=ConversionMode.DEFAULT,
):
    with source.open("rb") as f:
        if mode == ConversionMode.BINARY:
            data = f.read()

    width, height = derive_atlas_dimensions(len(data) / 4, width, height)

    if mode == ConversionMode.BINARY:
        image = Image.frombytes("RGBA", (width, height), data)

    image.save(dest)
