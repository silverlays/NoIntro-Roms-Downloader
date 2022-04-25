import os, sys
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

import archiveApi.archive_platforms as archive
from custom_widgets import MyTableWidget
from constants import *



app = QApplication(sys.argv)


class MainWindow(QMainWindow):
  platforms_data = []
  table = None

  def __init__(self, platforms_data: list, app: QApplication):
    super().__init__()
    self.platforms_data = sorted(platforms_data, key=lambda x: x.platform_name)

    self.setWindowTitle(f'{PROGRAM_TITLE} v{PROGRAM_VERSION}')
    self.setWindowIcon(QIcon(PROGRAM_ICON))
    self.setMinimumHeight(PROGRAM_HEIGHT)
    self.setMinimumWidth(PROGRAM_WIDTH)

    self.main_widget = QWidget(self)
    self.setCentralWidget(self.main_widget)
    self.main_layout = QHBoxLayout(self.main_widget)
    self.splitter = QSplitter(Qt.Orientation.Horizontal, self.main_widget)
    self.splitter.setMinimumWidth(10)
    self.main_layout.addWidget(self.splitter)

    self.loadStyle()
    self.setupMenu()
    self.setupLeft()
    self.setupRight()
    
    self.splitter.setSizes([100, 10])
    self.download_details_group.setHidden(True)
    self.platform_list_widget.setCurrentRow(0)

    self.show()
    sys.exit(app.exec())
  
  def loadStyle(self):
    if os.path.exists(PROGRAM_DEFAULT_STYLE):
      self.setStyleSheet(open(PROGRAM_DEFAULT_STYLE, 'r').read())
    else: print('<WARNING> Cannot load default style:', PROGRAM_DEFAULT_STYLE)

  def setupMenu(self):
    self.menubar = QMenuBar()
    self.menu_options = QMenu('Options', self.menubar)
    self.menu_help = QMenu('?', self.menubar)

    self.menu_action_settings = QAction('Settings', self.menu_options)
    self.menu_action_settings.triggered.connect(lambda: QMessageBox.critical(self, 'TODO!', 'No yet implemented.'))

    self.menu_action_help = QAction('Help', self.menu_help)
    self.menu_action_help.setShortcut(QKeySequence('F1'))
    self.menu_action_help.triggered.connect(lambda: QMessageBox.critical(self, 'TODO!', 'No yet implemented.'))

    self.menu_action_about_me = QAction('About Me...', self.menu_help)
    self.menu_action_about_me.triggered.connect(lambda: QMessageBox.critical(self, 'TODO!', 'No yet implemented.'))

    self.menu_action_about_qt = QAction('About Qt...', self.menu_help)
    self.menu_action_about_qt.triggered.connect(lambda: QMessageBox.aboutQt(self, 'About Qt...'))
    
    self.menu_options.addAction(self.menu_action_settings)
    self.menu_help.addAction(self.menu_action_help)
    self.menu_help.addSeparator()
    self.menu_help.addAction(self.menu_action_about_me)
    self.menu_help.addAction(self.menu_action_about_qt)
    self.menubar.addMenu(self.menu_options)
    self.menubar.addMenu(self.menu_help)

    self.setMenuBar(self.menubar)

  def setupLeft(self):
    self.left_group = QGroupBox('Platforms List', self)
    
    self.left_group_layout = QVBoxLayout(self.left_group)
    self.left_group_layout.setContentsMargins(0, 0, 0, 0)

    self.platform_list_widget = QListWidget(self.left_group)
    self.platform_list_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    self.platform_list_widget.currentItemChanged.connect(self.platformSelectedChanged)

    for platform in self.platforms_data:
      platform: archive.Platform
      list_item = QListWidgetItem(self.platform_list_widget)
      list_item.setText(f'{platform.platform_name}\n({platform.platform_updated})')
      list_item.setIcon(QIcon(PROGRAM_ICON))
      self.platform_list_widget.addItem(list_item)
    
    self.left_group_layout.addWidget(self.platform_list_widget)
    self.left_group.setLayout(self.left_group_layout)

    self.splitter.addWidget(self.left_group)
  
  def setupRight(self):
    self.right_group = QGroupBox('Platform Details')
    self.right_group_layout = QVBoxLayout(self.right_group)
    self.right_group_layout.setContentsMargins(0, 0, 0, 0)
    self.right_group_layout.addWidget(self.filterWidget(self.right_group))
    self.right_group_layout.addWidget(self.statusWidget(self.right_group))
    self.splitter.addWidget(self.right_group)
  
  def filterWidget(self, parent: QWidget) -> QWidget:
    widget = QWidget(parent)
    layout = QHBoxLayout(widget)
    layout.setContentsMargins(5, 5, 5, 5)
    layout.addWidget(QLabel('Filter:', widget))
    
    self.filter_editbox = QLineEdit(widget)
    self.filter_editbox.setClearButtonEnabled(True)
    self.filter_editbox.textEdited.connect(self.filterTextEdited)
    layout.addWidget(self.filter_editbox)
    return widget
  
  def statusWidget(self, parent: QWidget) -> QGroupBox:
    self.download_details_group = QGroupBox('Download Details', parent)
    layout = QGridLayout(self.download_details_group)
    
    download_label = QLabel('Current opération:', self.download_details_group)
    download_label.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
    layout.addWidget(download_label, 0, 0)
    
    self.status_download_label = QLabel('N/A')
    self.status_download_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
    self.status_download_label.setStyleSheet('margin-left: 100px')
    layout.addWidget(self.status_download_label, 0, 0)

    self.status_progressbar = QProgressBar(self.download_details_group)
    self.status_progressbar.setValue(0)
    layout.addWidget(self.status_progressbar, 1, 0, 1, 2)

    layout.addWidget(QLabel(''), 2, 0, 1, 2)

    button_pause = QPushButton('Pause', self.download_details_group)
    button_pause.setCursor(Qt.CursorShape.PointingHandCursor)
    button_pause.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Maximum)
    layout.addWidget(button_pause, 3, 0)
    button_stop = QPushButton('Stop', self.download_details_group)
    button_stop.setCursor(Qt.CursorShape.PointingHandCursor)
    button_stop.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Maximum)
    layout.addWidget(button_stop, 3, 1)

    return self.download_details_group

  def platformSelectedChanged(self, current: QListWidgetItem, previous: QListWidgetItem):
    if previous:
      font = previous.font()
      font.setBold(False)
      previous.setFont(font)

    font = current.font()
    font.setBold(True)
    current.setFont(font)

    if self.table: self.right_group_layout.removeWidget(self.table)
    platform: archive.Platform = self.platforms_data[self.platform_list_widget.currentIndex().row()]
    self.table = MyTableWidget()
    self.table.action_download.triggered.connect(self.downloadTriggered)
    for rom in platform.roms_data: self.table.addItem(rom)
    self.right_group_layout.insertWidget(1, self.table)
    self.filter_editbox.clear()

  def filterTextEdited(self, filter_text: str):
    if self.table:
      self.table.filterByKeyword(filter_text)

  def downloadTriggered(self, checked: bool):
    download_list = []
    for x in self.table.selectedItems():
      if x.column() == 0: download_list.append(f'{self.table.item(x.row(), 0).text()}.{self.table.item(x.row(), 2).text()}')
    # TODO