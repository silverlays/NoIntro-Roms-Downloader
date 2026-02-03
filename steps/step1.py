from PySide6.QtWidgets import QWidget, QVBoxLayout, QComboBox, QSpacerItem, QSizePolicy


class Step(QWidget):
    def __init__(self):
        super().__init__()

        self.subtitle = "Choose a platform:"

        layout = QVBoxLayout()

        platform_combo_box = QComboBox()
        platform_combo_box.addItems(["Platform 1", "Platform 2", "Platform 3"])

        spacer = QSpacerItem(
            10, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        layout.addWidget(platform_combo_box)
        layout.addSpacerItem(spacer)

        self.setLayout(layout)
