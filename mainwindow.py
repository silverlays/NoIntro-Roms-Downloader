from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

# Helpers
from _settings import SettingsHelper
from _updater import UpdaterHelper
from _platforms import PlatformsHelper
from _tools import Tools, RomDownload, Unzip
from _debug import *

# Ui
from ui.ui_MainWindow import Ui_MainWindow as Ui
from ui.ui_DownloadPane import Ui_DownloadPane

# Dialogs
from download_queue import DownloadQueue
from options import Options
from about import About



class DownloadPane(QWidget, Ui_DownloadPane):
  """This class made the jonction between the «Download_Pane.ui» and the main window."""
  def __init__(self, gb_parent: QGroupBox):
    super().__init__(gb_parent)
    self.setupUi(self)
    self.parent_gb_layout = QVBoxLayout()
    self.parent_gb_layout.addWidget(self)
    self.hide()



class MainWindow(QMainWindow, Ui):
  """This is the main window class."""
  def __init__(self, settings: SettingsHelper, updater: UpdaterHelper, platforms: PlatformsHelper):
    super().__init__()
    self.setupUi(self)

    # Setup local variables
    self.settings = settings
    self.updater = updater
    self.platforms = platforms
    self.optionsDialog = Options(self, settings)
    self.aboutDialog = About(self)
    self.download_pane = DownloadPane(self.gb_downloads)
    self.download_queue = DownloadQueue(self, self.platforms)

    # Setup form
    self.setWindowTitle(f"{self.windowTitle()} {self.updater.currentVersionString()}")
    self.tw_romsList.setColumnWidth(0, int(self.tw_romsList.width() / 2.42))
    self.tw_romsList.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
    self.gb_downloads.setLayout(self.download_pane.parent_gb_layout)

    # Setup statusbar
    self.statusbar_update = QLabel()
    self.statusbar.addPermanentWidget(self.statusbar_update)
    self.statusbar_queue = QLabel()
    self.statusbar_queue.setMinimumWidth(150)
    self.statusbar_queue.mousePressEvent = self.download_queue.show
    self.statusbar.addWidget(self.statusbar_queue)
    
    # Setup download queue
    self.download_queue.updatedListEvent = self._updateStatusbarQueueText
    self.download_queue.downloadClickedEvent = self._launchRomsDownload

    # Setup menu events
    self.actionShowOptions.triggered.connect(lambda: self.optionsDialog.show())
    self.actionExit.triggered.connect(lambda: self.close())
    self.actionGet_help.triggered.connect(lambda: QDesktopServices.openUrl(QUrl('https://github.com/silverlays/NoIntro-Roms-Downloader/wiki')))
    self.actionCheck_for_updates.triggered.connect(lambda: self._checkUpdates())
    self.actionAbout.triggered.connect(self.aboutDialog.show)
    self.actionAbout_Qt.triggered.connect(lambda: QMessageBox.aboutQt(self, 'About Qt...'))
    
    # Setup other events
    self.lw_platforms.itemClicked.connect(self._onListwidgetSelectionChanged)
    self.tw_romsList.customContextMenuRequested.connect(self._onRomslistRightClick)
    self.le_filter.textChanged.connect(self._filterTableWidget)
    self.pb_eur.toggled.connect(self._filterTableWidget)
    self.pb_usa.toggled.connect(self._filterTableWidget)
    self.pb_jpn.toggled.connect(self._filterTableWidget)
    self.pb_all.toggled.connect(self._filterTableWidget)
    self.gb_downloads.clicked.connect(self._onDownloadPaneClicked)

    # Startup task(s)
    self._checkUpdates(at_launch=True)
    self._loadPlatformsList()


  def _checkUpdates(self, at_launch: bool = False):
    """Check for software update.

    Args:
        at_launch (bool, optional): 'True' if the application just started. Defaults to False.
    """
    def Ask():
      answer = QMessageBox.question(self, "Update available", f"An update is available!\n\nActual version: {self.updater.currentVersionString()}\nLastest version: {self.updater.lastestVersionString()}\n\nWould you like to update now ?")
      if answer == QMessageBox.StandardButton.Yes:
        QMessageBox.warning(self, 'Updating...', 'Not yet implemented, sorry.')
        ###
        ### TODO: IMPLEMENT SOFTWARE UPDATE
        ###
      else:
        self.statusbar_update.setText("New version available!")

    update_available = self.updater.updateAvailable() if self.settings.get('check_updates') else False
    
    if at_launch and self.settings.get('check_updates') and update_available: Ask()
    elif at_launch and self.settings.get('check_updates') and not update_available: self.statusbar_update.setText("You are up-to-date.")
    elif not at_launch and update_available: Ask()
    elif not at_launch and not update_available:
      QMessageBox.information(self, "Update", "You are up-to-date.")
      self.statusbar_update.setText("You are up-to-date.")


  def _loadPlatformsList(self):
    for i in range(self.platforms.platformsCount()):
      name = self.platforms.getPlatformName(i)
      item = QListWidgetItem(QIcon(':/app.ico'), name)
      self.lw_platforms.addItem(item)


  def _filterTableWidget(self):
    """Handle table filtering."""
    # Made the RegEx
    keywords = self.le_filter.text()
    if self.pb_eur.isChecked(): keywords += " Europe"
    if self.pb_usa.isChecked(): keywords += " USA"
    if self.pb_jpn.isChecked(): keywords += " Japan"
    keywords = keywords.replace(' ', '.+')

    # Fill the table based on RegEx
    to_keep = [item for item in self.tw_romsList.findItems(keywords, Qt.MatchFlag.MatchRegularExpression)]
    for i in range(self.tw_romsList.rowCount()):
      self.tw_romsList.hideRow(i) if self.tw_romsList.item(i, 0) not in to_keep else self.tw_romsList.showRow(i)


  def _updateStatusbarQueueText(self):
    count = self.download_queue.getTotalCount()
    self.statusbar_queue.setText(f"<a href='#'>{count} item(s) in queue</a>") if count > 0 else self.statusbar_queue.setText("")


  def _addToQueue(self):
    self.download_queue.add(self.platforms.getPlatformName(self.lw_platforms.selectedIndexes()[0].row()), [row.row() for row in self.tw_romsList.selectedIndexes() if row.column() == 0])
    self._updateStatusbarQueueText()
  

  def _downloadNowContextMenu(self):
    self._addToQueue()
    self._launchRomsDownload()


  def _launchRomsDownload(self):
    DebugHelper.print(DebugType.TYPE_INFO, "Download started...")
    self.gb_downloads.setChecked(True)
    self.download_pane.show()
    total_count = self.download_queue.getTotalCount()
    self.download_pane.pb_progress.setMaximum(total_count)
    self.download_pane.pb_progress.setValue(0)
    for platform in self.download_queue.queue_dict:
      for i in range(len(self.download_queue.queue_dict[platform])):
        rom_name = self.platforms.getRomName(platform, self.download_queue.queue_dict[platform][0])
        rom_index = self.download_queue.queue_dict[platform][0]
        self.download_pane.l_job.setText(f"[{platform}] {rom_name}")
        self.download_pane.l_progress.setText(f"{i}/{total_count}")
        self.repaint()
        RomDownload(self.settings, self.platforms, platform, rom_index)
        if self.settings.get('unzip'): Unzip(self.settings, f"{rom_name}.{self.platforms.getRom(platform, rom_name)['format']}")
        self.download_queue.remove(platform, rom_index)
        self.download_pane.pb_progress.setValue(i+1)
        self.repaint()
    self.download_pane.l_job.setText("N/A")
    self.download_pane.l_progress.setText(f"{i+1}/{total_count}")


  def _onListwidgetSelectionChanged(self, item: QListWidgetItem):
    platform_name = item.text()

    # Clear the table
    self.tw_romsList.setRowCount(0)

    # Fill the table with new content
    for i in range(self.platforms.getRomsCount(platform_name)):
      rom_name = self.platforms.getRomName(platform_name, i)
      rom_data = self.platforms.getRom(platform_name, rom_name)

      # Creating Items for table's row
      rom_name_item = QTableWidgetItem(rom_name)
      rom_size_item = QTableWidgetItem(Tools.convertSizeToReadable(rom_data['size']))
      rom_size_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
      rom_format_item = QTableWidgetItem(rom_data['format'])
      rom_format_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
      rom_md5_item = QTableWidgetItem(rom_data['md5'])
      rom_md5_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
      rom_crc32_item = QTableWidgetItem(rom_data['crc32'].upper())
      rom_crc32_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
      rom_sha1_item = QTableWidgetItem(rom_data['sha1'])
      rom_sha1_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
      
      self.tw_romsList.insertRow(i)
      self.tw_romsList.setItem(i, 0, rom_name_item)
      self.tw_romsList.setItem(i, 1, rom_size_item)
      self.tw_romsList.setItem(i, 2, rom_format_item)
      self.tw_romsList.setItem(i, 3, rom_md5_item)
      self.tw_romsList.setItem(i, 4, rom_crc32_item)
      self.tw_romsList.setItem(i, 5, rom_sha1_item)
    
    # Resize columns and sort
    self.tw_romsList.resizeColumnsToContents()
    #self.tw_romsList.sortByColumn(0, Qt.SortOrder.AscendingOrder)

    # Apply any previous filters
    self._filterTableWidget()


  def _onDownloadPaneClicked(self):
    if self.gb_downloads.isChecked():
      self.download_pane.show()
      self.gb_downloads.setFixedHeight(100)
    else:
      self.download_pane.hide()
      self.gb_downloads.setFixedHeight(20)


  def _onRomslistRightClick(self, point: QPoint):
    menu = QMenu(self.tw_romsList)
    
    add_to_queue = QAction("Add to Queue")
    add_to_queue.triggered.connect(lambda: self._addToQueue())

    download_now = QAction("Download Now")
    download_now.triggered.connect(lambda: self._downloadNowContextMenu())
    
    menu.exec([add_to_queue, download_now], QCursor.pos(), parent=self.tw_romsList)
