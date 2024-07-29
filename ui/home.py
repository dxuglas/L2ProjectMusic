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


class RecomendationPanel(QFrame):
  def __init__(self, parent) -> None:
    super().__init__(parent)

    self.setObjectName("ReccomendationPanel")

    self.layout = QGridLayout()
    self.layout.setContentsMargins(10, 10, 10, 10)
    self.setLayout(self.layout)

    self.songs = SongRecomendations().from_library(4)


class SongArt(QPushButton):
  def __init__(self, parent, song):
    super().__init__(parent)
    self.parent = parent
    self.song = song

    self.setObjectName("song_art")
    self.setFlat(True)

  def resizeEvent(self, a0: QResizeEvent | None) -> None:
    self.setFixedSize(QSize(self.parent.height(), self.parent.height()))
    self.setIconSize(QSize(self.width(), self.height()))


class SongPanel(QFrame):
  def __init__(self, parent, song = None):
    super().__init__(parent)
    self.song = song
    self.parent = parent

    self.setObjectName("SongPanel")

    self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)

    self.layout = QHBoxLayout()
    self.layout.setContentsMargins(0, 0, 0, 0)
    self.setLayout(self.layout)

    self.art = SongArt(self, song)
    self.name = QLabel(objectName = "name")

    if song:
      self.load()
    else:
      self.art.setIcon(QIcon(r"ui\assets\placeholder.svg"))
      self.name.setText("Song")

    self.layout.addWidget(self.art)
    self.layout.addWidget(self.name, alignment = Qt.AlignmentFlag.AlignLeft)

  def load(self):
    song_data = LoadSong(self.song)
    
    request = requests.get(image_url)

    pixmap = QPixmap()
    pixmap.loadFromData(request.content)

    icon = QIcon(pixmap)
    self.icon_changer.setIcon(icon)
    self.icon_changer.setIconSize(QSize(self.icon_changer.width(), 
                                        self.icon_changer.height()))

  
