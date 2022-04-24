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
    self.loadStyle()
    self.setupMenu()
    self.setupLeft()
    self.setupRight()
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
    self.menu_action_about_me.setShortcut(QKeySequence('Ctrl+A'))
    self.menu_action_about_me.triggered.connect(lambda: QMessageBox.critical(self, 'TODO!', 'No yet implemented.'))

    self.menu_action_about_qt = QAction('About Qt...', self.menu_help)
    self.menu_action_about_qt.setShortcut(QKeySequence('Ctrl+Q'))
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
    self.left_group = QGroupBox('Platform', self)
    self.left_group.setFixedWidth(int(PROGRAM_WIDTH / 3))
    
    self.left_group_layout = QVBoxLayout(self.left_group)
    self.left_group_layout.setContentsMargins(0, 0, 0, 0)

    self.platform_list_widget = QListWidget(self.left_group)
    self.platform_list_widget.setCursor(Qt.CursorShape.PointingHandCursor)
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

    self.main_layout.addWidget(self.left_group, alignment=Qt.AlignmentFlag.AlignLeft)
  
  def setupRight(self):
    self.right_group = QGroupBox('Games')
    self.right_group_layout = QVBoxLayout(self.right_group)
    self.right_group_layout.setContentsMargins(0, 0, 0, 0)
    self.main_layout.addWidget(self.right_group, stretch=1)
  
  def platformSelectedChanged(self, current: QListWidgetItem, previous: QListWidgetItem):
    if previous:
      font = previous.font()
      font.setBold(False)
      previous.setFont(font)

    font = current.font()
    font.setBold(True)
    current.setFont(font)

    platform: archive.Platform = self.platforms_data[self.platform_list_widget.currentIndex().row()]
    old_table = self.right_group_layout.itemAt(0).widget() if hasattr(self.right_group_layout.itemAt(0), 'widget') else None
    new_table = MyTableWidget()
    for rom in platform.roms_data: new_table.addItem(rom)
    self.right_group_layout.removeWidget(old_table)
    self.right_group_layout.addWidget(new_table)
