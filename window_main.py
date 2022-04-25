import os, sys
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

import archive_api as archive
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

    self.widget_main = QWidget(self)
    self.setCentralWidget(self.widget_main)
    self.layout_main = QHBoxLayout(self.widget_main)
    self.splitter_main = QSplitter(Qt.Orientation.Horizontal, self.widget_main)
    self.splitter_main.setMinimumWidth(10)
    self.layout_main.addWidget(self.splitter_main)

    self.loadStyle()
    self.setupMenu()
    self.setupLeft()
    self.setupRight()
    
    self.splitter_main.setSizes([100, 10])
    self.group_download_details.setHidden(True)
    self.widget_platform_list.setCurrentRow(0)

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
    group_left = QGroupBox('Platforms List', self)
    
    layout_left_group = QVBoxLayout(group_left)
    layout_left_group.setContentsMargins(0, 0, 0, 0)

    self.widget_platform_list = QListWidget(group_left)
    self.widget_platform_list.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    self.widget_platform_list.currentItemChanged.connect(self.platformSelectedChanged)

    for platform in self.platforms_data:
      platform: archive.Platform
      list_item = QListWidgetItem(self.widget_platform_list)
      list_item.setText(f'{platform.platform_name}\n({platform.platform_updated})')
      list_item.setIcon(QIcon(PROGRAM_ICON))
      self.widget_platform_list.addItem(list_item)
    
    layout_left_group.addWidget(self.widget_platform_list)
    group_left.setLayout(layout_left_group)

    self.splitter_main.addWidget(group_left)
  
  def setupRight(self):
    group_right = QGroupBox('Platform Details')
    self.layout_right_group = QVBoxLayout(group_right)
    self.layout_right_group.setContentsMargins(0, 0, 0, 0)
    self.layout_right_group.addWidget(self.filterWidget(group_right))
    self.layout_right_group.addWidget(self.statusWidget(group_right))
    self.splitter_main.addWidget(group_right)
  
  def filterWidget(self, parent: QWidget) -> QWidget:
    widget_filter = QWidget(parent)
    layout_filter = QHBoxLayout(widget_filter)
    layout_filter.setContentsMargins(5, 5, 5, 5)
    layout_filter.addWidget(QLabel('Filter:', widget_filter))
    
    self.editbox_filter = QLineEdit(widget_filter)
    self.editbox_filter.setClearButtonEnabled(True)
    self.editbox_filter.textEdited.connect(self.filterTextEdited)
    layout_filter.addWidget(self.editbox_filter)
    return widget_filter
  
  def statusWidget(self, parent: QWidget) -> QGroupBox:
    self.group_download_details = QGroupBox('Download Details', parent)
    layout_download_details = QGridLayout(self.group_download_details)
    
    label_download = QLabel('Current opération:', self.group_download_details)
    label_download.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
    layout_download_details.addWidget(label_download, 0, 0)
    
    self.label_status_download = QLabel('N/A')
    self.label_status_download.setAlignment(Qt.AlignmentFlag.AlignLeft)
    self.label_status_download.setStyleSheet('margin-left: 100px')
    layout_download_details.addWidget(self.label_status_download, 0, 0)

    self.progressbar_status = QProgressBar(self.group_download_details)
    self.progressbar_status.setValue(0)
    layout_download_details.addWidget(self.progressbar_status, 1, 0, 1, 2)

    layout_download_details.addWidget(QLabel(''), 2, 0, 1, 2)

    button_pause = QPushButton('Pause', self.group_download_details)
    button_pause.setCursor(Qt.CursorShape.PointingHandCursor)
    button_pause.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Maximum)
    layout_download_details.addWidget(button_pause, 3, 0)
    button_stop = QPushButton('Stop', self.group_download_details)
    button_stop.setCursor(Qt.CursorShape.PointingHandCursor)
    button_stop.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Maximum)
    layout_download_details.addWidget(button_stop, 3, 1)

    return self.group_download_details

  def platformSelectedChanged(self, current: QListWidgetItem, previous: QListWidgetItem):
    if previous:
      font = previous.font()
      font.setBold(False)
      previous.setFont(font)

    font = current.font()
    font.setBold(True)
    current.setFont(font)

    if self.table: self.layout_right_group.removeWidget(self.table)
    platform: archive.Platform = self.platforms_data[self.widget_platform_list.currentIndex().row()]
    self.table = MyTableWidget()
    self.table.action_download.triggered.connect(self.downloadTriggered)
    for rom in platform.roms_data: self.table.addItem(rom)
    self.layout_right_group.insertWidget(1, self.table)
    self.editbox_filter.clear()

  def filterTextEdited(self, filter_text: str):
    if self.table:
      self.table.filterByKeyword(filter_text)

  def downloadTriggered(self, checked: bool):
    download_list = []
    for x in self.table.selectedItems():
      if x.column() == 0: download_list.append(f'{self.table.item(x.row(), 0).text()}.{self.table.item(x.row(), 2).text()}')
    # TODO