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

from media_handler.song_recomendations import SongRecomendations
from file_handler.load import LoadSong


class HomePage(QFrame):
  def __init__(self, parent) -> None:
    super().__init__(parent)

    self.setObjectName("HomePage")
    self.setStyleSheet(open(r"ui\stylesheets\home.qss").read())

    self.layout = QVBoxLayout()
    self.layout.setContentsMargins(10, 10, 10, 10)
    self.setLayout(self.layout)

    self.recommendation_panel = RecomendationPanel(self)
    self.layout.addWidget(self.recommendation_panel, stretch = 1)
    self.layout.addStretch(2)


class DisplayPanel(QFrame):
  def __init__(self, parent) -> None:
    super().__init__(parent)

    self.setObjectName("DisplayPanel")

    self.layout = QGridLayout()
    self.layout.setContentsMargins(10, 10, 10, 10)
    self.setLayout(self.layout)

    self.songs = SongRecomendations().from_library(4)
    self.title = QLabel(objectName = "title")

    self.layout.addWidget(self.title, 0, 0, 1, 2)
    self.layout.setSpacing(15)

    for x in range(1, 3):
      for y in range(2):
        panel = SongPanel(self, self.songs[x+y-1])
        self.layout.addWidget(panel, x, y)

  def resizeEvent(self, a0: QResizeEvent | None) -> None:
    font = self.title.font()
    font.setPointSize(int(self.height()/8))
    self.title.setFont(font)

class RecomendationPanel(DisplayPanel):
  def __init__(self, parent) -> None:
    super().__init__(parent)
    self.songs = SongRecomendations().from_library(4)
    self.title.setText("Songs from your Library")

class SimilarSongsPanel(DisplayPanel):
  def __init__(self, parent) -> None:
    super().__init__(parent)
    self.song = None
    while not self.song:
      self.song = SongRecomendations().from_library(1)[0]
      
    self.songs = None
    self.title.setText(f"Because you liked... {self.song}")

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
    data = LoadSong(self.song)
    
    self.name.setText(data.name)
    self.art.setIcon(data.icon)

  def resizeEvent(self, a0: QResizeEvent | None) -> None:
    font = self.name.font()
    font.setPointSize(int(self.height()/5))
    self.name.setFont(font)
