from PyQt6.QtWidgets import (
  QFrame, 
  QHBoxLayout,
  QVBoxLayout,
  QGridLayout,
  QPushButton,
  QLabel,
  QScrollArea,
  QSizePolicy
)
from PyQt6.QtCore import (
  QSize,
  Qt
)
from PyQt6.QtGui import (
  QIcon,
  QResizeEvent
)

class PlaylistPage(QFrame):
  def __init__(self, parent, playlist = None) -> None:
    super().__init__(parent)
    self.playlist = playlist

    self.setObjectName("PlaylistPage")
    self.setStyleSheet(open(r"ui\stylesheets\playlist.qss").read())

    self.layout = QVBoxLayout()
    self.layout.setContentsMargins(10, 10, 10, 10)
    self.setLayout(self.layout)

    self.header = HeaderPanel(self, self.playlist)
    self.song_viewer = SongViewer(self, self.playlist)

    self.layout.addWidget(self.header, stretch=1)
    self.layout.addWidget(self.song_viewer, stretch=2)


class HeaderPanel(QFrame):
  def __init__(self, parent, playlist) -> None:
    super().__init__(parent)
    self.playlist = playlist
    
    self.setObjectName("HeaderPanel")
    self.setSizePolicy(QSizePolicy.Policy.Expanding,
                       QSizePolicy.Policy.Expanding)
    
    self.layout = QHBoxLayout()
    self.setLayout(self.layout)

    self.art = PlaylistArt(self, playlist)
    self.art.setSizePolicy(QSizePolicy.Policy.Expanding,
                           QSizePolicy.Policy.Expanding)

    self.name = QPushButton(objectName = "name", flat = True)

    self.layout.addWidget(self.art, stretch=1)
    self.layout.addWidget(self.name, stretch=2)

    if playlist:
      self.load()
    else:
      self.art.setIcon(QIcon(r"ui\assets\placeholder.svg"))
      self.name.setText("Playlist")
    
  def load(self):
    self.art.setIcon(QIcon(self.playlist["icon"]))
    self.name.setText(self.playlist["name"])


class PlaylistArt(QPushButton):
  def __init__(self, parent, playlist):
    super().__init__(parent)
    self.playlist = playlist
  
    self.setObjectName("art")
    self.setFlat(True)

  def resizeEvent(self, a0: QResizeEvent | None) -> None:
    self.setFixedWidth(self.height())
    
    if self.playlist:
      self.setIconSize(QSize(self.width(), self.height()))
    else:
      self.setIconSize(QSize(int(self.width()/2), int(self.height()/2)))
      

class SongViewer(QFrame):
  def __init__(self, parent, playlist):
    super().__init__(parent)
    self.playlist = playlist