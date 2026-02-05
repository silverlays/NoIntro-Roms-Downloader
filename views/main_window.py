from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QMenuBar,
    QMenu,
    QMessageBox,
)

from .components import CustomPushButton


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initial Setup
        self._setupUi()
        self._setupMenuBar()

        # Window properties
        self.resize(1024, 768)

        # Window events

        ### Widgets Events

    def aboutURD(self):
        QMessageBox.about(
            self,
            "About Universal Roms Downloader",
            """<h1><u>Universal Roms Downloader</u></h1>
<p>This software is about a software who do... some stuff<p>
<p>...</p>
<p>And made by Silv3r btw.<p>
""",
        )

    def _setupMenuBar(self):
        self.menubar = QMenuBar()

        # About Actions
        self.about_qt_action = QAction("About Qt")
        self.about_urd_action = QAction("About Universal Roms Downloader")

        self.about_menu = QMenu("About")
        self.about_menu.addAction(self.about_urd_action)
        self.about_menu.addAction(self.about_qt_action)

        self.menubar.addMenu(self.about_menu)

        self.setMenuBar(self.menubar)

    def _setupUi(self):
        # Main Widget
        self.central_widget = QWidget()
        self.central_layout = QVBoxLayout()
        self.central_widget.setLayout(self.central_layout)
        self.central_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Top Widget
        self.top_widget = QWidget()
        self.top_widget.setObjectName("topWidget")
        self.top_layout = QHBoxLayout()
        self.top_widget.setLayout(self.top_layout)
        self.central_layout.addWidget(self.top_widget)

        ## Title Label
        self.title_label = QLabel("[Page Name]")
        self.title_label.setObjectName("pageTitleLabel")
        self.top_layout.addWidget(self.title_label)

        ## Spacer
        self.top_layout.addStretch()

        ## Close Button
        self.close_button = CustomPushButton()
        self.close_button.setObjectName("closeButton")
        self.close_button.setIcon(QIcon(":/assets/close.svg"))
        self.close_button.setFlat(True)
        self.top_layout.addWidget(self.close_button)

        # View Widget
        self.view_widget = QWidget()
        self.view_widget.setObjectName("viewWidget")
        self.view_layout = QGridLayout()
        self.view_widget.setLayout(self.view_layout)
        self.view_layout.setContentsMargins(0, 50, 0, 0)
        self.central_layout.addWidget(self.view_widget)

        # Navigation Widget
        self.navigation_widget = QWidget()
        self.navigation_widget.setObjectName("navigationWidget")
        self.navigation_layout = QHBoxLayout()
        self.navigation_widget.setLayout(self.navigation_layout)
        self.central_layout.addWidget(self.navigation_widget)

        ## TODO Navigation buttons

        # Finalization
        self.setCentralWidget(self.central_widget)
