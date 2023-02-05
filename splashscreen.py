import os, time
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

# Helpers
from _settings import *
from _updater import *
from _platforms import *
from _tools import *
from _debug import *



class SplashScreen(QSplashScreen):
  settings: SettingsHelper
  updater: UpdaterHelper
  platforms: PlatformsHelper


  def __init__(self, app: QApplication):
    super().__init__(flags=Qt.WindowType.WindowStaysOnTopHint)

    self.app = app
    self.settings = SettingsHelper()
    self.updater = UpdaterHelper()

    self.setPixmap(QPixmap(':/splash.png'))


  def show(self):
    super().show()

    # Check cache validity and presence. If not, build it.
    if not os.path.exists(PLATFORMS_CACHE_FILENAME):
      DebugHelper.print(DebugType.TYPE_WARNING, f"<{PLATFORMS_CACHE_FILENAME}> not found. Download needed.", "SPLASHSCREEN")
      cache = CacheGenerator(self.app, self)
      cache.run()
    elif not Tools.isCacheValid(self.settings.get('cache_expiration')):
      DebugHelper.print(DebugType.TYPE_WARNING, f"<{PLATFORMS_CACHE_FILENAME}> is outdated. Download needed.", "SPLASHSCREEN")
      cache = CacheGenerator(self.app, self)
      cache.run()
    else:
      self.showMessage("Loading data, please wait...",
        color=Qt.GlobalColor.white,
        alignment=(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignCenter)
      )
      time.sleep(2)
    self.platforms = PlatformsHelper()
    super().close()


  def mousePressEvent(self, a0: QMouseEvent) -> None:
    '''
    Overrided to avoid splashscreen being hided
    '''
    return
