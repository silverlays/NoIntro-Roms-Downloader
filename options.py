from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

# Ui
from ui.ui_Options import Ui_Dialog as Ui

# Helpers
from _settings import SettingsHelper


class Options(QDialog, Ui):
  _settings: SettingsHelper

  def __init__(self, parent, settings: SettingsHelper):
    super().__init__(parent)
    self._settings = settings
    
    # Setup UI
    self.setupUi(self)
    self.setWindowFlag(Qt.WindowType.MSWindowsFixedSizeDialogHint, True)
    
    # Setup events
    self.pb_BrowsePath.clicked.connect(self._onBrowsePathClicked)
    self.accepted.connect(self._onAccept)
  

  def show(self) -> None:
    # Cache expiration
    cache_expiration = self._settings.get('cache_expiration')
    cache_expiration = str(cache_expiration) if cache_expiration != 0 else "<none>"
    self.cb_cache_expiration.setCurrentText(cache_expiration)

    # Download path
    self.le_DownloadPath.setText(self._settings.get('download_path'))
    
    # Decompress after download
    self.cb_unzip.setChecked(self._settings.get('unzip'))
    
    # Check for updates at startup
    self.cb_checkupdates.setChecked(self._settings.get('check_updates'))
    return super().show()


  def _onBrowsePathClicked(self):
    new_path = QFileDialog.getExistingDirectory()
    if new_path != "": self.le_DownloadPath.setText(new_path)


  def _onAccept(self):
    import os

    # Cache expiration
    cache_expiration = self.cb_cache_expiration.currentText()
    cache_expiration = int(cache_expiration) if cache_expiration != "<none>" else 0
    self._settings.update(['cache_expiration', cache_expiration])

    # Download path
    if os.path.isdir(self.le_DownloadPath.text()):
      self._settings.update(['download_path', self.le_DownloadPath.text()])

    # Decompress after download
    self._settings.update(['unzip', self.cb_unzip.isChecked()])

    # Check for updates at startup
    self._settings.update(['check_updates', self.cb_checkupdates.isChecked()])
    
    # Write settings
    self._settings.write()
