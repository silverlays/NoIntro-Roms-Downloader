from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow

from .ui.mainwindow_ui import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Window properties
        self.setWindowFlags(Qt.WindowType.MSWindowsFixedSizeDialogHint)

        ### Widgets Events
