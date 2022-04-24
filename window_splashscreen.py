from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

import archiveApi.archive_platforms as archive


class DownloadWorker(QObject):
  platform: archive.Platform = None
  finished = pyqtSignal(archive.Platform)

  def __init__(self, platform: archive.Platform) -> None:
    super().__init__(None)
    self.platform = platform
  
  def run(self):
    self.platform.roms_data = archive.download_platform_files(self.platform.platform_id)
    self.finished.emit(self.platform)


class SplashScreen(QSplashScreen):
  app: QApplication = None
  platforms_data = []
  threads = []
  workers = []
  download_completed = 0

  def __init__(self, app: QApplication) -> None:
    super().__init__()
    self.app = app
    self.setPixmap(QPixmap('./splash.png'))
    self.show()
  
  def show(self) -> None:
    super().show()
    self.showMessage('Downloading platforms list...', color=Qt.GlobalColor.white, alignment=(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter))
    platforms = archive.download_platforms()
    
    # DEBUG
    platforms.pop()
    platforms.pop()
    platforms.pop()
    platforms.pop()
    platforms.pop()
    platforms.pop()
    platforms.pop()
    platforms.pop()
    platforms.pop()
    platforms.pop()
    platforms.pop()
    platforms.pop()
    platforms.pop()
    platforms.pop()
    platforms.pop()
    platforms.pop()
    platforms.pop()
    platforms.pop()
    # DEBUG
    
    [self.threads.append(QThread()) for _ in range(len(platforms))]

    for i in range(len(self.threads)):
      id, name, updated = platforms[i].values()
      self.workers.append(DownloadWorker(archive.Platform(id, name, updated)))
      self.workers[i].moveToThread(self.threads[i])
      self.threads[i].started.connect(self.workers[i].run)
      self.workers[i].finished.connect(self._updateMessage)
      self.workers[i].finished.connect(self.threads[i].quit)
      self.threads[i].finished.connect(self.threads[i].deleteLater)
      self.threads[i].start()
    
    while self.download_completed != len(self.threads): self.app.processEvents()
    self.close()
    
  def _updateMessage(self, platform_data: archive.Platform):
    self.download_completed += 1
    self.platforms_data.append(platform_data)
    self.showMessage(f'Downloading data... ({(self.download_completed):02d}/{len(self.threads):02d})', color=Qt.GlobalColor.white, alignment=(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter))
