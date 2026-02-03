from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class SettingsData:
    download_folder: Path


class Settings:
    def __init__(self):
        # TODO Write settings code
        pass
