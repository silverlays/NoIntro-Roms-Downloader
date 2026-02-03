from PySide6.QtCore import Qt
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout

from ui.mainwindow_ui import Ui_MainWindow
from step_widget_handler import StepTemplate


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.step_handler = StepTemplate()

        # Window properties
        self.setWindowFlag(Qt.WindowType.CustomizeWindowHint, True)
        self.setWindowFlag(Qt.WindowType.MSWindowsFixedSizeDialogHint, True)

        ### Widgets Events
        self.closeLabel.mousePressEvent = self.on_mouse_press_event

        self.centralFrame.setLayout(self.step_handler.loadStepLayout())  # type: ignore

    def on_mouse_press_event(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.close()
