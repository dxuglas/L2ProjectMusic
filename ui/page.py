from PyQt6.QtGui import QResizeEvent
from PyQt6.QtWidgets import (
  QFrame, 
  QVBoxLayout
)

from .playlist import PlaylistPage


class PageHandler(QFrame):
  def __init__(self, parent) -> None:
    super().__init__(parent)
    self.parent = parent

    self.setObjectName("PageHandler")
    self.setStyleSheet(open(r"ui\stylesheets\page.qss").read())

    self.width = int(parent.screen_size[0] - int(parent.screen_size[0]*0.066))
    self.setMinimumWidth(self.width)
    
    self.layout = QVBoxLayout()

    self.page = PlaylistPage(self)
    self.layout.addWidget(self.page)

  def resizeEvent(self, a0: QResizeEvent | None) -> None: 
    self.page.resizeEvent(a0) 
    return super().resizeEvent(a0)

