from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout


class ViewTemplate(QWidget):
    def __init__(self, title: str, description: str):
        super().__init__()

        self.title = title

        # Description Label
        self.description = QLabel(description)
        self.description.setObjectName("viewDescriptionLabel")
        self.description.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.main_layout.addWidget(self.description)

        self.setLayout(self.main_layout)
