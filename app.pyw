import sys, os
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

# Helpers
from _debug import *

# Main class
from splashscreen import SplashScreen
from mainwindow import MainWindow

# darktheme package
import qdarktheme as darktheme



os.environ['DEBUG'] = "4" # 0 = TO DESACTIVATE
                          # 1 = ERROR ONLY
                          # 2 = ERROR + WARNING
                          # 3 = ERROR + WARNING + INFO
                          # 4 = ERROR + WARNING + INFO + DEBUG



if __name__ == '__main__':
  # Initialize PyQt
  app = QApplication(sys.argv)

  # Load theme and ressources
  darktheme.setup_theme()
  QResource.registerResource('resources.rcc')

  # Show the splashscreen and do starting stuff
  splash = SplashScreen(app)
  splash.show()

  # Initialize main window
  mainWindow = MainWindow(splash.settings, splash.updater, splash.platforms)
  mainWindow.show()

  # Execute then shutdown
  sys.exit(app.exec())
