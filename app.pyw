import sys
from PyQt6.QtWidgets import QApplication

from window_splashscreen import SplashScreen
from window_main import MainWindow

app = QApplication(sys.argv)


if __name__ == '__main__':
  splash = SplashScreen(app)
  MainWindow(splash.platforms_data, app)
