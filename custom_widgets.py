import typing
from PyQt6.QtCore import *
from PyQt6.QtWidgets import QWidget, QTableWidget, QTableWidgetItem

from constants import size_format



class MyTableWidgetItem(QTableWidgetItem):
  def __init__(self, text: str, not_center: bool = False):
    super().__init__(text, QTableWidgetItem.ItemType.Type)
    if not not_center: self.setTextAlignment(Qt.AlignmentFlag.AlignHCenter)


class MyTableWidget(QTableWidget):  
  def __init__(self):
    super().__init__(None)
    self.setSelectionBehavior(self.SelectionBehavior.SelectRows)
    
    for i in range(0, 6):  self.insertColumn(i)
    self.setHorizontalHeaderItem(0, QTableWidgetItem('GAME'))
    self.setHorizontalHeaderItem(1, QTableWidgetItem('SIZE'))
    self.setHorizontalHeaderItem(2, QTableWidgetItem('FORMAT'))
    self.setHorizontalHeaderItem(3, QTableWidgetItem('MD5'))
    self.setHorizontalHeaderItem(4, QTableWidgetItem('CRC32'))
    self.setHorizontalHeaderItem(5, QTableWidgetItem('SHA1'))
    
    self.setColumnWidth(0, 390) # GAME
    self.setColumnWidth(1, 70) # SIZE
    self.setColumnWidth(2, 70) # FORMAT
    self.setColumnWidth(3, 70) # MD5
    self.setColumnWidth(4, 70) # CRC32
    self.setColumnWidth(5, 70) # SHA1
    self.verticalHeader().hide()

  def addItem(self, rom_details: dict) -> None:
    row = self.rowCount()
    self.insertRow(row)
    self.setItem(row, 0, MyTableWidgetItem(rom_details['name'], not_center=True))
    self.setItem(row, 1, MyTableWidgetItem(f'{size_format(rom_details["size"])}'))
    self.setItem(row, 2, MyTableWidgetItem(rom_details['format']))
    self.setItem(row, 3, MyTableWidgetItem(rom_details['md5']))
    self.setItem(row, 4, MyTableWidgetItem(rom_details['crc32']))
    self.setItem(row, 5, MyTableWidgetItem(rom_details['sha1']))


