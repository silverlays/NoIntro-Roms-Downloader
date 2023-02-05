from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

# Helpers
from _platforms import PlatformsHelper

# Ui
from ui.ui_DownloadQueue import Ui_DownloadQueue



class DownloadQueue(QDialog, Ui_DownloadQueue):
  """This class handle the Download Queue"""
  queue_dict = {}
  platforms: PlatformsHelper = None


  def __init__(self, parent: QMainWindow, platforms: PlatformsHelper):
    super().__init__(parent)
    self.setupUi(self)
    self.platforms = platforms


  def show(self) -> None:
    self.listWidget.clear()
    for i in self.queue_dict.keys():
      self.listWidget.addItems([f"[{i}] {self.platforms.getRomName(i, x)}" for x in self.queue_dict[i]])
    return super().show()


  def add(self, platform_name: str, roms_indexes: list[int]) -> None:
    try: self.queue_dict[platform_name] += roms_indexes
    except KeyError: self.queue_dict[platform_name] = roms_indexes
    finally: self.queue_dict[platform_name] = sorted(self.queue_dict[platform_name])


  def remove(self, platform_name: str, roms_indexes: list[int]) -> None:
    for i in roms_indexes:
      try: self.queue_dict[platform_name].remove(i)
      except ValueError: pass


  def getTotalCount(self) -> int:
    count = 0
    for i in self.queue_dict.keys():
      count += len(self.queue_dict[i])
    return count
