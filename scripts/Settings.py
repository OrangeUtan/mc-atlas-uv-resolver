from dataclasses import dataclass, field
from pathlib import Path

import yaml
from dataclasses_json import dataclass_json
from dataclasses_json.cfg import config


@dataclass_json
@dataclass
class Settings:
    minecraft_install_root: Path = field(metadata=config(decoder=Path))
    atlases_root: Path = field(metadata=config(decoder=Path))

    @classmethod
    def load(cls, path: Path) -> "Settings":
        with path.open("r") as f:
            return cls.from_dict(yaml.safe_load(f))

    def get_version_assets_root(self, minecraft_version: str):
        return self.minecraft_install_root / "versions" / minecraft_version / "assets"
