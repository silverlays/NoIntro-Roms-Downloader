import config

from PySide6.QtCore import QEvent, Qt, QObject
from PySide6.QtWidgets import QWidget, QGridLayout

from models import Settings
from views import MainWindow, SettingsView


class WidgetsController(QObject):
    def __init__(self):
        super().__init__()

        # Models
        self.settings = Settings()

        ## MainWindow
        self.main_window = MainWindow()
        self.main_window.setWindowTitle(
            f"{config.PROGRAM_NAME} - v{config.VERSION_STRING}"
        )

        # Views
        self.views_widget = QWidget()
        self.views_widget_layout = QGridLayout()
        self.views_widget.setLayout(self.views_widget_layout)
        self.main_window.centralwidget.layout().addWidget(self.views_widget)  # type: ignore

        # Events
        self.main_window.closeLabel.installEventFilter(self)

    def load(self):
        # FIXME For debug purposes only
        self.settings_view = SettingsView()
        self.views_widget_layout.addWidget(self.settings_view, 0, 0)
        self.main_window.show()

    def eventFilter(self, watched: QObject, event: QEvent):
        if watched == self.main_window.closeLabel:
            if event.type() == QEvent.Type.MouseButtonRelease and event.button() == Qt.MouseButton.LeftButton:  # type: ignore
                self.main_window.close()

        return super().eventFilter(watched, event)
