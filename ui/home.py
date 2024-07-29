from PyQt6.QtWidgets import (
  QFrame,
  QVBoxLayout,
  QGridLayout,
  QSizePolicy,
  QHBoxLayout,
  QLabel,
  QPushButton
)

from PyQt6.QtGui import (
  QIcon,
  QResizeEvent
)

from PyQt6.QtCore import (
  Qt,
  QSize
)

from media_handler.song_recommendations import SongRecommendations
from file_handler.load import LoadSong


class HomePage(QFrame):
  def __init__(self, parent) -> None:
    super().__init__(parent)

    self.setObjectName("HomePage")
    self.setStyleSheet(open(r"ui\stylesheets\home.qss").read())

    self.layout = QVBoxLayout()
    self.layout.setContentsMargins(10, 10, 10, 10)
    self.setLayout(self.layout)

    self.recommendation_panel = RecommendationPanel(self)
    self.similar_song_panel = SimilarSongsPanel(self)

    self.layout.addWidget(self.recommendation_panel, stretch = 1)
    self.layout.addWidget(self.similar_song_panel, stretch = 1)
    self.layout.addStretch(1)


class DisplayPanel(QFrame):
  def __init__(self, parent, songs) -> None:
    super().__init__(parent)

    self.setObjectName("DisplayPanel")

    self.layout = QGridLayout()
    self.layout.setContentsMargins(10, 10, 10, 10)
    self.setLayout(self.layout)

    self.songs = songs
    self.title = QLabel(objectName = "title")

    self.layout.addWidget(self.title, 0, 0, 1, 2)
    self.layout.setSpacing(10)

    for x in range(2):
      for y in range(2):
        panel = SongPanel(self, self.songs[2*x+y])
        self.layout.addWidget(panel, x+1, y)

  def resizeEvent(self, a0: QResizeEvent | None) -> None:
    font = self.title.font()
    font.setPointSize(int(self.height()/8))
    self.title.setFont(font)


class RecommendationPanel(DisplayPanel):
  def __init__(self, parent) -> None:
    super().__init__(parent, SongRecommendations().from_library(4))
    self.title.setText("Songs from your Library")


class SimilarSongsPanel(DisplayPanel):
  def __init__(self, parent) -> None:
    self.song = None
    while not self.song:
      self.song = LoadSong(SongRecommendations().from_library(1)[0])
      
    self.songs = SongRecommendations().from_shazam(self.song.key, 4)

    super().__init__(parent, self.songs)
    self.title.setText(f"Because you liked... {self.song.name}")


class SongArt(QPushButton):
  def __init__(self, parent, song):
    super().__init__(parent)
    self.parent = parent
    self.song = song

    self.setObjectName("SongArt")

  def resizeEvent(self, a0: QResizeEvent | None) -> None:
    self.setFixedSize(QSize(self.parent.height(), self.parent.height()))
    self.setIconSize(QSize(self.width(), self.height()))


class SongPanel(QFrame):
  def __init__(self, parent, song = None):
    super().__init__(parent)
    self.song = song
    self.parent = parent

    self.setObjectName("SongPanel")

    self.setSizePolicy(QSizePolicy.Policy.Preferred, 
                       QSizePolicy.Policy.Expanding)

    self.layout = QHBoxLayout()
    self.layout.setContentsMargins(0, 0, 0, 0)
    self.setLayout(self.layout)

    self.art = SongArt(self, song)
    self.name = QLabel(objectName = "name")

    if song:
      self.load()
    else:
      self.art.setIcon(QIcon(r"ui\assets\placeholder.svg"))
      self.name.setText("Try Uploading More Songs!")

    self.layout.addWidget(self.art)
    self.layout.addWidget(self.name, alignment = Qt.AlignmentFlag.AlignLeft)

  def load(self):
    if isinstance(self.song, str):  
      data = LoadSong(self.song)
    elif isinstance(self.song, dict):
      data = LoadSong(None, self.song)
    
    self.name.setText(data.name)
    self.art.setIcon(data.icon)

  def resizeEvent(self, a0: QResizeEvent | None) -> None:
    font = self.name.font()
    font.setPointSize(int(self.height()/5))
    self.name.setFont(font)
