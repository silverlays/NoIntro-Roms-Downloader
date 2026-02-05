from PySide6.QtCore import Slot
from PySide6.QtWidgets import QFileDialog

from .template import ControllerTemplate
from views import DownloadFolderView


class DownloadFolderController(ControllerTemplate[DownloadFolderView]):
    def __init__(self):
        super().__init__(DownloadFolderView())
        self.View.browse_button.clicked.connect(self.on_browse_button_clicked)

    @Slot()
    def on_browse_button_clicked(self):
        QFileDialog.getExistingDirectory(None, "Select the ROM download directory")
