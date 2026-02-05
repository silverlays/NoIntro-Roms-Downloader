import config

from PySide6.QtCore import QObject, Slot
from PySide6.QtWidgets import QMessageBox

from models import Settings
from views import MainWindow


class MainController(QObject):
    def __init__(self):
        super().__init__()

        # Models
        self.settings = Settings()

        ## MainWindow
        self.main_window = MainWindow()
        self.main_window.setWindowTitle(
            f"{config.PROGRAM_NAME} - v{config.VERSION_STRING}"
        )

        # Events
        self.main_window.about_qt_action.triggered.connect(
            lambda: QMessageBox.aboutQt(self.main_window, "About Qt")
        )
        self.main_window.about_urd_action.triggered.connect(self.main_window.aboutURD)
        self.main_window.close_button.clicked.connect(self.main_window.close)

    def load(self):
        # TODO Will be adapted when settings will be implemented.
        from controllers.downloadFolder_controller import DownloadFolderController

        self.controller = DownloadFolderController()
        self.controller.InvoqueNextView.connect(self._on_invoke_next_view)
        self.main_window.view_layout.addWidget(self.controller.View, 0, 0)
        self.main_window.title_label.setText(self.controller.View.title)
        self.main_window.show()

    @Slot()
    def _on_invoke_next_view(self):
        print("Next view invoqued!")
