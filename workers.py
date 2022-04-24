from time import sleep
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

import archiveApi.archive_platforms as archive
from custom_widgets import MyTableWidget


class LoadingWorker(QObject):
  def __init__(self):
    super().__init__(None)
  
  def run():
    pass