from PyQt6.QtWidgets import (
  QFrame, 
  QPushButton, 
  QHBoxLayout, 
  QVBoxLayout, 
  QGridLayout,
  QSlider,
  QLabel,
  QSizePolicy
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

    self.playing_info = PlayingInfo(self)
    self.layout.addWidget(self.playing_info, 
                          alignment = Qt.AlignmentFlag.AlignLeft,
                          stretch = 3)
    
    self.media_controls = MediaControls(self)
    self.layout.addWidget(self.media_controls, stretch = 2)

    self.volume_controls = VolumeControls(self)
    self.layout.addWidget(self.volume_controls, stretch = 3)


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


class MediaControls(QFrame):
  def __init__(self, parent):
    super().__init__(parent)
    
    self.setObjectName("MediaControls")
    
    self.layout = QHBoxLayout()
    self.setLayout(self.layout)

    self.shuffle_btn = QPushButton(objectName = "shuffle_btn", flat = True,
                                   icon = QIcon(r"ui\assets\shuffle.svg"))
    
    self.track_back_btn = QPushButton(objectName = "track_back_btn", 
                                      flat = True,
                                      icon = QIcon(r"ui\assets\bw_track.svg"))
    
    self.pause_play_btn = QPushButton(objectName = "pause_play_btn", 
                                      flat = True,
                                      icon = QIcon(r"ui\assets\pause.svg"))
    
    self.track_forward_btn = QPushButton(objectName = "track_forward_btn", 
                                         flat = True,
                                         icon = QIcon(r"ui\assets\fw_track.svg"))
    
    self.loop_btn = QPushButton(objectName = "loop_btn", flat = True,
                                  icon = QIcon(r"ui\assets\loop.svg"))
    
    self.layout.addWidget(self.shuffle_btn)
    self.layout.addWidget(self.track_back_btn)
    self.layout.addWidget(self.pause_play_btn)
    self.layout.addWidget(self.track_forward_btn)
    self.layout.addWidget(self.loop_btn)

  def resizeEvent(self, a0: QResizeEvent | None) -> None:
    self.setFixedWidth(self.width())

    self.shuffle_btn.setFixedHeight(self.shuffle_btn.width())
    self.track_back_btn.setFixedHeight(self.track_back_btn.width())
    self.pause_play_btn.setFixedHeight(self.pause_play_btn.width())
    self.track_forward_btn.setFixedHeight(self.track_forward_btn.width())
    self.loop_btn.setFixedHeight(self.loop_btn.width())

    self.shuffle_btn.setIconSize(QSize(self.shuffle_btn.width(), self.shuffle_btn.width()))
    self.track_back_btn.setIconSize(QSize(self.track_back_btn.width(), self.track_back_btn.width()))
    self.pause_play_btn.setIconSize(QSize(self.pause_play_btn.width(), self.pause_play_btn.width()))
    self.track_forward_btn.setIconSize(QSize(self.track_forward_btn.width(), self.track_forward_btn.width()))
    self.loop_btn.setIconSize(QSize(self.loop_btn.width(), self.loop_btn.width()))

class VolumeControls(QFrame):
  def __init__(self, parent):
    super().__init__(parent)
    
    self.setObjectName("VolumeControls")

    self.layout = QHBoxLayout()
    self.setLayout(self.layout)