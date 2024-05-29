from PyQt6.QtWidgets import (
  QFrame, 
  QHBoxLayout,
  QVBoxLayout
)

from .playlist import PlaylistPage


class PageHandler(QFrame):
  def __init__(self, parent):
    super().__init__(parent)
    self.parent = parent

    self.setObjectName("PageHandler")
    self.setStyleSheet(open(r"ui\stylesheets\page.qss").read())

    self.width = int(parent.screen_size[0] - int(parent.screen_size[0]*0.066))
    self.setMinimumWidth(self.width)

    self.layout = QVBoxLayout()

    self.layout.addWidget(PlaylistPage(self))

