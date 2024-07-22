from PyQt6.QtWidgets import (
  QFrame, 
  QPushButton,
  QVBoxLayout,
  QScrollArea
)
from PyQt6.QtCore import (
  QSize,
  Qt
)
from PyQt6.QtGui import QIcon, QResizeEvent

from .popups.playlist_creation import CreationPopup
from file_handler.load import Playlists 


class Library(QFrame):
  def __init__(self, parent) -> None:
    super().__init__(parent)
    self.parent = parent

    self.setObjectName("Library")
    self.setStyleSheet(open(r"ui\stylesheets\library.qss").read())
    
    self.width = int(self.parent.screen_size[0]*0.05)
    self.setFixedWidth(self.width)

    self.layout = QVBoxLayout()
    self.setLayout(self.layout)

    self.menu_buttons = MenuButtons(self)
    self.layout.addWidget(self.menu_buttons)

    self.playlists_scroller = PlaylistScroller(self)
    self.layout.addWidget(self.playlists_scroller)


class MenuButtons(QFrame):
  def __init__(self, parent):
    super().__init__(parent)
    self.setObjectName("MenuButtons")

    self.layout = QVBoxLayout()
    self.layout.setContentsMargins(10, 5, 10, 5)
    self.layout.setSpacing(10)
    self.setLayout(self.layout)

    self.home_btn = QPushButton(objectName = "home_btn", flat = True,
                                icon = QIcon(r"ui\assets\home.svg"))
    
    self.search_btn = QPushButton(objectName = "search_btn", flat = True,
                                  icon = QIcon(r"ui\assets\search.svg"))
    
    self.new_btn = QPushButton(objectName = "new_btn", flat = True,
                               icon=QIcon(r"ui\assets\plus.svg"))
    self.new_btn.clicked.connect(self.new)

    self.layout.addWidget(self.home_btn)
    self.layout.addWidget(self.search_btn)
    self.layout.addWidget(self.new_btn)

  def resizeEvent(self, a0: QResizeEvent | None) -> None:
    self.home_btn.setIconSize(QSize(self.home_btn.width(), 
                                    self.home_btn.width()))
    self.search_btn.setIconSize(QSize(self.search_btn.width(), 
                                    self.search_btn.width()))
    self.new_btn.setIconSize(QSize(self.new_btn.width(),
                                   self.new_btn.width()))
    
  def new(self):
    self.popup = CreationPopup(self.window())
    self.popup.show()

class PlaylistButton(QPushButton):
  def __init__(self, parent, playlist) -> None:
    super().__init__(parent)
    self.parent = parent
    self.playlist = playlist

    self.setObjectName("PlaylistButton")

    print(playlist["icon"])
    self.setIcon(QIcon(playlist["icon"]))
    self.setFlat(True)

    self.window = self.window()
    self.clicked.connect(self.load_playlist)

  def load_playlist(self):
    self.window.update_page(self.playlist)

  def resizeEvent(self, a0: QResizeEvent | None) -> None:
    self.setFixedSize(QSize(self.parent.width(), self.parent.width()))
    self.setIconSize(QSize(self.width(), self.height()))


class PlaylistScroller(QScrollArea):
  def __init__(self, parent) -> None:
    super().__init__(parent)
    self.playlists = Playlists().load()

    self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

    self.layout = QVBoxLayout()
    self.layout.setContentsMargins(0, 0, 0, 0)
    self.frame = QFrame(self, objectName = "playlists")
    self.frame.setLayout(self.layout)

    for playlist in self.playlists:
      self.layout.addWidget(PlaylistButton(self, playlist), 
                            alignment=Qt.AlignmentFlag.AlignCenter)

    self.layout.addStretch(1)
    self.setWidget(self.frame)
    self.setWidgetResizable(True)




