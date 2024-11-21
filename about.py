from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog

# Ui
from ui.ui_About import Ui_About as Ui



class About(QDialog, Ui):
  def __init__(self, parent):
    super().__init__(parent)
    self.setupUi(self)
    self.setWindowFlag(Qt.WindowType.MSWindowsFixedSizeDialogHint, True)