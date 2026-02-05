import app_rc
import config
import sys
from PySide6.QtCore import QFile
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from controllers import MainController


if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = MainController()

    app.setOrganizationName("INFORLAC")
    app.setApplicationName(config.PROGRAM_NAME)
    app.setApplicationVersion(config.VERSION_STRING)
    app.setWindowIcon(QIcon(":/assets/app_icon.svg"))

    # FIXME Direct call of QSS only for debug, DON'T keep it for deployment.

    # stylesheet = QFile(":/app.qss")
    stylesheet = QFile("app.qss")
    if stylesheet.open(QFile.OpenModeFlag.ReadOnly):
        app.setStyleSheet(stylesheet.readAll().toStdString())

    controller.load()

    sys.exit(app.exec())
