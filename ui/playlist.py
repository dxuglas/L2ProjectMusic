from PyQt6.QtWidgets import (
  QFrame, 
  QHBoxLayout,
  QVBoxLayout,
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

from file_handler.load import LoadSong

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

    self.layout.addWidget(self.header, stretch=5)
    self.layout.addWidget(self.song_viewer, stretch=6)

class HeaderPanel(QFrame):
  def __init__(self, parent, playlist) -> None:
    super().__init__(parent)
    self.playlist = playlist
    
    self.setObjectName("HeaderPanel")
    
    self.layout = QHBoxLayout()
    self.setLayout(self.layout)

    self.art = PlaylistArt(self, playlist)
    self.art.setSizePolicy(QSizePolicy.Policy.Expanding,
                           QSizePolicy.Policy.Expanding)

    self.name = QPushButton(objectName = "name", flat = True)
    self.desc = QLabel(objectName = "desc")

    self.layout.addWidget(self.art, stretch=1)

    self.text_layout = QVBoxLayout()
    self.text_layout.setContentsMargins(0, 0, 0, 0)

    self.text_layout.addStretch(1)
    self.text_layout.addWidget(self.name, alignment=Qt.AlignmentFlag.AlignLeft, stretch=1)
    self.text_layout.addWidget(self.desc, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop, stretch=1)

    self.text_container = QFrame()
    self.text_container.setLayout(self.text_layout)

    self.layout.addWidget(self.text_container, stretch = 2)

    if playlist:
      self.load()
    else:
      self.art.setIcon(QIcon(r"ui\assets\placeholder.svg"))
      self.name.setText("Playlist")
      self.desc.setText("")
    
  def load(self):
    self.art.setIcon(QIcon(self.playlist["icon"]))
    self.name.setText(self.playlist["name"])
    self.desc.setText(self.playlist["description"])

  def resizeEvent(self, a0: QResizeEvent | None) -> None:
    font = self.name.font()
    font.setPointSize(int(self.height()/7))
    self.name.setFont(font)

class PlaylistArt(QPushButton):
  def __init__(self, parent, playlist):
    super().__init__(parent)
    self.playlist = playlist
  
    self.setObjectName("playlist_art")
    self.setFlat(True)

    self.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)

  def resizeEvent(self, a0: QResizeEvent | None) -> None:
    self.setFixedWidth(self.height())
    
    if self.playlist:
      self.setIconSize(QSize(self.width(), self.height()))
    else:
      self.setIconSize(QSize(int(self.width()/2), int(self.height()/2)))


class SongPanel(QFrame):
  def __init__(self, parent, song = None):
    super().__init__(parent)
    self.song = song
    self.parent = parent

    self.setObjectName("SongPanel")

    self.sized = False
    self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)

    self.layout = QHBoxLayout()
    self.layout.setContentsMargins(0, 0, 0, 0)
    self.setLayout(self.layout)

    self.art = SongArt(self, song)
    self.name = QLabel(objectName = "name")
    self.artist = QLabel(objectName = "artist")

    if song:
      self.load()
    else:
      self.art.setIcon(QIcon(r"ui\assets\placeholder.svg"))
      self.name.setText("Song")
      self.artist.setText("Artist")

    self.layout.addWidget(self.art)
    self.layout.addWidget(self.name, alignment = Qt.AlignmentFlag.AlignCenter)
    self.layout.addWidget(self.artist, alignment = Qt.AlignmentFlag.AlignCenter)

  def load(self):
    song_data = LoadSong(self.song)
    self.art.setIcon(song_data.icon)
    self.name.setText(song_data.name)
    self.artist.setText(song_data.artist)

  def resizeEvent(self, a0: QResizeEvent | None) -> None:
    if not self.sized:
      self.sized = True
      self.setMinimumHeight(int(self.parent.height()/5))
    self.setFixedHeight(self.height())


class SongArt(QPushButton):
  def __init__(self, parent, song):
    super().__init__(parent)
    self.parent = parent
    self.song = song

    self.setObjectName("song_art")
    self.setFlat(True)

  def resizeEvent(self, a0: QResizeEvent | None) -> None:
    self.setFixedSize(QSize(self.parent.height(), self.parent.height()))

    if self.song:
      self.setIconSize(QSize(self.width(), self.height()))
    else:
      self.setIconSize(QSize(int(self.width()/2), int(self.height()/2)))


class SongViewer(QScrollArea):
  def __init__(self, parent, playlist):
    super().__init__(parent)
    self.playlist = playlist

    self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

    self.layout = QVBoxLayout()
    self.frame = QFrame(self, objectName = "songs")
    self.frame.setLayout(self.layout)

    for song in self.playlist["songs"]:
      widget = SongPanel(self, song)
      self.layout.addWidget(widget)

    self.layout.addStretch(1)
    self.setWidget(self.frame)
    self.setWidgetResizable(True)

  def resizeEvent(self, a0: QResizeEvent | None) -> None:
    self.frame.setFixedWidth(self.width())
    self.setMinimumHeight(self.height())