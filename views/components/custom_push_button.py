from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton, QSizePolicy


class CustomPushButton(QPushButton):
    def __init__(self, text: str | None = None):
        super().__init__(text)

        # Button properties
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        # self.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
