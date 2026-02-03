import app_rc
import config
import sys
from PySide6.QtCore import QFile
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from controllers.widgets_controller import WidgetsController


if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = WidgetsController()

    app.setOrganizationName("INFORLAC")
    app.setApplicationName(config.PROGRAM_NAME)
    app.setApplicationVersion(config.VERSION_STRING)
    app.setWindowIcon(QIcon(":/assets/app_icon.svg"))

    stylesheet = QFile(":/app.qss")
    if stylesheet.open(QFile.OpenModeFlag.ReadOnly):
        app.setStyleSheet(stylesheet.readAll().toStdString())

    controller.load()

    sys.exit(app.exec())
