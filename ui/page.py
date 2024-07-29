from PyQt6.QtWidgets import (
  QFrame, 
  QVBoxLayout,
  QSizePolicy
)

from qframelesswindow import (
  TitleBar as QTitleBar
)

from .playlist import PlaylistPage
from .home import HomePage


class PageHandler(QFrame):
  def __init__(self, parent) -> None:
    super().__init__(parent)
    self.setObjectName("PageHandler")
    self.setStyleSheet(open(r"ui\stylesheets\page.qss").read())
    self.setSizePolicy(QSizePolicy.Policy.Expanding,
                       QSizePolicy.Policy.Expanding)
    
    self.title_bar = QTitleBar(self)
    
    self.layout = QVBoxLayout()
    self.layout.setContentsMargins(0, self.title_bar.frameGeometry().height(), 
                                   0, 0)
    self.setLayout(self.layout)

    self.page = HomePage(self)
    self.layout.addWidget(self.page)
    self.status = "home"

  def update_page(self, type, data = None):
    if self.page:
      self.page.deleteLater()
      self.page = None
    if type == "playlist":
      self.page = PlaylistPage(self, data)
      self.layout.addWidget(self.page)
    elif type == "home":
      self.page = HomePage(self)
      self.layout.addWidget(self.page)
    
    self.status = type

class TitleBar(QTitleBar):
  def __init__(self, parent) -> None:
    super().__init__(parent)
