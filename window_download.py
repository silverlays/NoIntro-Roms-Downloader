from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *



class DownloadWindow(QDialog):
  is_ok = False
  download_list = []


  def __init__(self, parent: QWidget, download_list: list) -> None:
    super().__init__(parent)

    self.download_list = download_list

    self.setModal(True)
    self.setWindowTitle('Download(s) list confirmation')
    #self.setStyleSheet('border: 1px solid white')

    layout_main = QVBoxLayout(self)

    label_title = QLabel('Please verify downloads and click OK', self)
    layout_main.addWidget(label_title, alignment=Qt.AlignmentFlag.AlignHCenter)

    scrollarea = QScrollArea(self)
    scrollarea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    widget_scrollarea = QWidget(scrollarea)
    widget_scrollarea.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)
    layout_widget_scrollarea = QVBoxLayout(widget_scrollarea)
    layout_widget_scrollarea.setContentsMargins(5, 5, 15, 5)
    layout_widget_scrollarea.setAlignment(Qt.AlignmentFlag.AlignTop)

    for i in range(len(download_list)): layout_widget_scrollarea.addWidget(self.downloadItemWidget(widget_scrollarea, download_list[i]), alignment=Qt.AlignmentFlag.AlignTop)

    widget_scrollarea.setLayout(layout_widget_scrollarea)
    scrollarea.setWidget(widget_scrollarea)
    layout_main.addWidget(scrollarea)
    layout_main.addWidget(self.buttonsWidget(self))

    self.setLayout(layout_main)
    self.show()
  
  def downloadItemWidget(self, parent: QWidget, item_name: str) -> QFrame:
    widget_item = QWidget(parent)
    widget_item.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)
    layout_item = QGridLayout(widget_item)
    layout_item.setContentsMargins(0, 0, 0, 0)
    layout_item.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)

    label_item = QLabel(item_name, widget_item)
    layout_item.addWidget(label_item, 0, 0, Qt.AlignmentFlag.AlignLeft)

    button_delete = QPushButton('X')
    button_delete.setCursor(Qt.CursorShape.PointingHandCursor)
    button_delete.setStyleSheet('margin-left: 20px; padding: 0; min-width: 20px; color: white; background-color: red')
    button_delete.clicked.connect(lambda: self.deleteClicked(widget_item, label_item.text()))
    layout_item.addWidget(button_delete, 0, 1, Qt.AlignmentFlag.AlignRight)

    widget_item.setLayout(layout_item)
    
    return widget_item
  
  def buttonsWidget(self, parent: QWidget) -> QWidget:
    widget = QWidget(parent)
    layout = QHBoxLayout(widget)

    button_ok = QPushButton('OK', widget)
    button_ok.setCursor(Qt.CursorShape.PointingHandCursor)
    button_ok.clicked.connect(self.okClicked)
    layout.addWidget(button_ok, alignment=Qt.AlignmentFlag.AlignLeft)

    button_cancel = QPushButton('Cancel', widget)
    button_cancel.setCursor(Qt.CursorShape.PointingHandCursor)
    button_cancel.clicked.connect(self.cancelClicked)
    layout.addWidget(button_cancel, alignment=Qt.AlignmentFlag.AlignRight)

    return widget
  
  def deleteClicked(self, widget: QWidget, game_name):
    self.download_list.remove(game_name)
    parent: QWidget = widget.parent()
    widget.hide()
    parent.setMinimumWidth(parent.width())
    parent.adjustSize()

  def okClicked(self):
    self.is_ok = True
    self.close()
  
  def cancelClicked(self):
    self.close()
