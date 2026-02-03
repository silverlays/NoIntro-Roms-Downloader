import sys
from PySide6.QtCore import Qt, QFile
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

import app_rc
from mainwindow import MainWindow

PROGRAM_NAME = "Universal Roms Downloader"
VERSION_MAJOR = 1
VERSION_MINOR = 0
VERSION_PATCH = 0

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    # stylesheet = QFile(":/app.css")
    stylesheet = QFile("app.css")

    if stylesheet.open(QFile.OpenModeFlag.ReadOnly):
        window.setStyleSheet(stylesheet.readAll().toStdString())

    app.setOrganizationName("INFORLAC")
    app.setApplicationName(PROGRAM_NAME)
    window.setWindowTitle(
        f"{PROGRAM_NAME} v{VERSION_MAJOR}.{VERSION_MINOR}.{VERSION_PATCH}"
    )
    window.setWindowIcon(QIcon(":/assets/app_icon.svg"))
    window.show()

    sys.exit(app.exec())
