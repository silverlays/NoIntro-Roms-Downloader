import config

from PySide6.QtCore import QObject

from models import Settings
from views import MainWindow


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

        # Events
        self.main_window.close_button.clicked.connect(self.main_window.close)

    def load(self):
        # TODO Will be adapted when settings will be implemented.
        from views import DownloadFolderView

        view = DownloadFolderView()
        self.main_window.title_label.setText(view.title)
        self.main_window.view_layout.addWidget(view, 0, 0)
        self.main_window.show()
