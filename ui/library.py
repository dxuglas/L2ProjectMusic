from PyQt6.QtWidgets import (
  QFrame, 
  QPushButton,
  QVBoxLayout,
  QLabel,
  QScrollArea,
  QWidget
)
from PyQt6.QtCore import (
  QSize,
  Qt
)
from PyQt6.QtGui import QIcon

from file_handler.load import Playlists

class Library(QFrame):
  def __init__(self, parent) -> None:
    super().__init__(parent)
    self.parent = parent

    self.setObjectName("Library")
    self.setStyleSheet(open(r"ui\stylesheets\library.qss").read())
    
    self.width = int(self.parent.screen_size[0]*0.049)
    self.setFixedWidth(self.width)

    self.layout = QVBoxLayout()
    self.layout.setContentsMargins(0, 0, 0, 0)
    self.setLayout(self.layout)

    self.layout.addWidget(MenuContainer(self), 
                         alignment=Qt.AlignmentFlag.AlignTop)
    self.layout.addWidget(PlaylistScroller(self))

class MenuContainer(QFrame):
  def __init__(self, parent) -> None:
    super().__init__(parent)

    self.size = int(parent.parent.screen_size[0] * 0.027)
    self.wmargins = int(parent.parent.screen_size[0] * 0.012)

    self.layout = QVBoxLayout()
    #self.layout.setContentsMargins(self.wmargins, 
     #                              int(parent.parent.screen_size[0]*0.006), 
    #                               self.wmargins, 0)
    self.setLayout(self.layout)

    self.home_btn = QPushButton(objectName = "home_btn",
                                icon = QIcon(r"ui\assets\home.svg"),
                                flat = True, 
                                size = QSize(self.size, self.size), 
                                iconSize = QSize(self.size, self.size))
    self.search_btn = QPushButton(objectName = "search_btn",
                                  icon = QIcon(r"ui\assets\search.svg"),
                                  flat = True, 
                                  size = QSize(self.size, self.size), 
                                  iconSize = QSize(self.size, self.size))
    
    self.layout.addWidget(self.home_btn)
    self.layout.addWidget(self.search_btn)

class PlaylistButton(QPushButton):
  def __init__(self, parent, playlist) -> None:
    super().__init__(parent)

    self.setIcon(QIcon(playlist["icon"]))
    self.setIconSize(QSize(60, 60))
    self.setFixedSize(60, 60)
    self.setFlat(True)

class PlaylistScroller(QScrollArea):
  def __init__(self, parent) -> None:
    super().__init__(parent)

    self.setFixedWidth(parent.width)
    self.playlists = Playlists().load()

    self.frame = QFrame(self, objectName = "playlists")
    self.layout = QVBoxLayout()
    self.frame.setLayout(self.layout)
    self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

    for playlist in self.playlists:
      self.layout.addWidget(PlaylistButton(self, playlist), alignment=Qt.AlignmentFlag.AlignCenter)
    for playlist in self.playlists:
      self.layout.addWidget(PlaylistButton(self, playlist), alignment=Qt.AlignmentFlag.AlignCenter)

    self.setWidget(self.frame)
    self.setWidgetResizable(True)




