from PyQt6.QtWidgets import (
  QFrame, 
  QPushButton, 
  QHBoxLayout, 
  QVBoxLayout, 
  QGridLayout,
  QSlider,
  QLabel
)
from PyQt6.QtCore import (
  QSize, 
  Qt
)
from PyQt6.QtGui import QIcon, QResizeEvent


class MediaInterface(QFrame):
  def __init__(self, parent, song = None) -> None:
    super().__init__(parent)
    self.parent = parent
    self.song = song
    
    self.setObjectName("MediaInterface")
    self.setStyleSheet(open(r"ui\stylesheets\media_interface.qss").read())

    self.height = (int(self.parent.screen_size[0] * 0.05))
    self.setFixedHeight(self.height)

    self.layout = QHBoxLayout()
    self.setLayout(self.layout)

    self.layout.addWidget(PlayingInfo(self), 
                          alignment = Qt.AlignmentFlag.AlignLeft)


class PlayingInfo(QFrame):
  def __init__(self, parent, song = None) -> None:
    super().__init__(parent)
    self.song = song

    self.setObjectName("PlayingInfo")

    self.layout = QHBoxLayout()
    self.layout.setSpacing(3)
    self.layout.setContentsMargins(0,0,0,0)
    self.setLayout(self.layout)

    self.art = PlayingArt(self, song)

    self.text_layout = QVBoxLayout()
    self.text_layout.setSpacing(0)
    self.text_layout.setContentsMargins(7, 7, 7, 7)

    self.name = QLabel(objectName = "name")
    self.artist = QLabel(objectName = "artist")

    self.text_layout.addWidget(self.name)
    self.text_layout.addWidget(self.artist)

    if self.song:
      self.load()
    else:
      self.art.setIcon(QIcon(r"ui\assets\placeholder.svg"))
      self.name.setText("Song Name")
      self.artist.setText("Artist Name")

    self.layout.addWidget(self.art)
    self.layout.addLayout(self.text_layout)

  def load(self):
    pass


class PlayingArt(QPushButton):
  def __init__(self, parent, song):
    super().__init__(parent)
    self.parent = parent
    self.song = song

    self.setObjectName("PlayingArt")
    self.setFlat(True)

  def resizeEvent(self, a0: QResizeEvent | None) -> None:
    self.setFixedSize(QSize(self.parent.height(), self.parent.height()))
    
    if self.song:
      self.setIconSize(QSize(self.width(), self.height()))
    else:
      self.setIconSize(QSize(int(self.width()/2), int(self.height()/2)))

