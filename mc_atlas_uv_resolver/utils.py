from pathlib import Path
from typing import Iterable

__all__ = ["flatten_paths"]


def flatten_paths(paths: Iterable[Path]):
    flattened: list[Path] = []
    for p in paths:
        if p.is_file():
            flattened.append(p)
        else:
            flattened.extend(p.iterdir())
    return flattened
