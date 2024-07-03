from PyQt6.QtWidgets import (
  QFrame, 
  QVBoxLayout,
  QSizePolicy
)

from qframelesswindow import (
  TitleBar as QTitleBar
)

from .playlist import PlaylistPage


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

    self.page = PlaylistPage(self)
    #self.layout.addWidget(self.page)

  def update_page(self, data):
    self.page.deleteLater()
    self.page = PlaylistPage(self, data)
    self.layout.addWidget(self.page)

class TitleBar(QTitleBar):
  def __init__(self, parent) -> None:
    super().__init__(parent)
