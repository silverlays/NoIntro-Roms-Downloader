from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class _SettingsData:
    first_run: bool = True
    download_folder: Path | None = None


class SettingsModel:
    def __init__(self):
        # TODO Write settings code.
        pass
