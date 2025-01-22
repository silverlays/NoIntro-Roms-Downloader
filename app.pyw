import sys, os
from PySide6.QtCore import QResource
from PySide6.QtWidgets import QApplication

# Helpers
from _constants import *
from _debug import *

# Main class
from splashscreen import SplashScreen
from mainwindow import MainWindow


os.environ['DEBUG'] = "4" # 0 = DISABLE
                          # 1 = ERROR
                          # 2 = WARNING
                          # 3 = INFO
                          # 4 = DEBUG



if __name__ == '__main__':
  # Initialize PyQt
  app = QApplication(sys.argv)
  QResource.registerResource(RESOURCES_FILE)
  
  # Show the splashscreen and do starting stuff
  splash = SplashScreen(app)
  splash.show()

    # Initialize main window
    mainWindow = MainWindow(splash.settings, splash.updater, splash.platforms)
    mainWindow.show()

    # Execute then shutdown
    sys.exit(app.exec())
