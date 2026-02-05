from pathlib import Path

from PySide6.QtCore import QSettings


class _UserSettings:
    def __init__(self, first_run: bool = True, download_folder: str = ".") -> None:
        self.FirstRun = first_run
        self.DownloadFolder = download_folder

    @property
    def FirstRun(self):
        return self._first_run

    @FirstRun.setter
    def FirstRun(self, value: bool):
        self._first_run = value

    @property
    def DownloadFolder(self):
        return self._download_folder.absolute().__str__()

    @DownloadFolder.setter
    def DownloadFolder(self, value: str):
        if Path(value).exists():
            self._download_folder = Path(value)
        else:
            self._download_folder = Path(".")


class SettingsModel(QSettings):
    def __init__(self):
        # TODO Write settings code.
        super().__init__()
        self.user_settings = _UserSettings()
        self.loadSettings()

    def loadSettings(self):
        self.user_settings.FirstRun = self.value(
            "first_run", self.user_settings.FirstRun, bool
        )  # type: ignore
        self.user_settings.DownloadFolder = self.value(
            "download_folder", self.user_settings.DownloadFolder, str
        )  # type: ignore

    def saveSettings(self):
        self.setValue("first_run", self.user_settings.FirstRun)
        self.setValue("download_folder", self.user_settings.DownloadFolder)
