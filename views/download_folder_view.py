from PySide6.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QFileDialog

from .components import ViewTemplate, CustomPushButton


class DownloadFolderView(ViewTemplate):
    def __init__(self):
        super().__init__(
            "Download Folder",
            "Choose the root folder where the ROMS will be downloaded :",
        )

        # Download Widget
        self.download_widget = QWidget()
        self.download_layout = QHBoxLayout()
        self.download_widget.setLayout(self.download_layout)

        ## Download Line Edit
        self.download_line_edit = QLineEdit()
        self.download_layout.addWidget(self.download_line_edit)

        ## Download Browse Button
        self.browse_button = CustomPushButton("...")
        self.browse_button.setFixedWidth(40)
        self.browse_button.clicked.connect(self.on_browse_button_clicked)
        self.download_layout.addWidget(self.browse_button)

        # Finalization
        self.main_layout.addWidget(self.download_widget)

    def on_browse_button_clicked(self):
        # TODO Must complete settings before ending this.
        QFileDialog.getExistingDirectory(None, "Select the ROM download directory")
