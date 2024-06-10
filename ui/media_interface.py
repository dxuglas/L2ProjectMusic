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
from PyQt6.QtGui import QIcon


class MediaInterface(QFrame):
  def __init__(self, parent) -> None:
    super().__init__(parent)
    self.parent = parent
    
    self.setObjectName("MediaInterface")
    self.setStyleSheet(open(r"ui\stylesheets\media_interface.qss").read())

    self.setFixedHeight(int(self.parent.screen_size[0] * 0.046))

    self.layout = QHBoxLayout()
    self.layout.setContentsMargins(10, 0, 10, 0)
    self.setLayout(self.layout)

    self.controls_layout = QVBoxLayout()
    self.controls_layout.setContentsMargins(0, int(self.parent.screen_size[0] 
                                                   * 0.007),  0, 
                                               int(self.parent.screen_size[0] 
                                                   * 0.007))

    self.controls_layout.addWidget(MediaControls(self), 
                                   alignment = Qt.AlignmentFlag.AlignCenter)
    self.controls_layout.addWidget(ProgressBar(self), 
                                   alignment = Qt.AlignmentFlag.AlignCenter)
    
    self.controls_container = QFrame()
    self.controls_container.setLayout(self.controls_layout)
    self.layout.addWidget(SongInfo(self))
    self.layout.addWidget(self.controls_container, alignment=Qt.AlignmentFlag.AlignCenter)
    self.layout.addWidget(VolumeControls(self), alignment=Qt.AlignmentFlag.AlignRight)


class MediaControls(QFrame):
  def __init__(self, parent) -> None:
    super().__init__(parent)

    self.setObjectName("MediaControls")
    
    self.height = int(parent.parent.screen_size[0] * 0.02)
    self.setFixedHeight(int(self.height * 0.9))
    self.setFixedWidth(int(self.height * 8))
    
    self.layout = QHBoxLayout()
    self.layout.setContentsMargins(0, 0, 0, 0)
    self.setLayout(self.layout)

    self.shuffle_btn = QPushButton(objectName = "shuffle_track_btn",
                                   icon = QIcon(r"ui\assets\shuffle.svg"),
                                   flat = True, 
                                   size = QSize(self.height, self.height), 
                                   iconSize = QSize(self.height, self.height))

    self.bw_track_btn = QPushButton(objectName = "bw_track_btn",
                                    icon = QIcon(r"ui\assets\bw_track.svg"), 
                                    flat = True, 
                                    size = QSize(self.height, self.height), 
                                    iconSize = QSize(self.height, self.height))

    self.pause_play_btn = QPushButton(objectName = "pause_play_btn",
                                      icon = QIcon(r"ui\assets\play.svg"),
                                      flat = True, 
                                      size = QSize(self.height, self.height), 
                                      iconSize = QSize(self.height, 
                                                       self.height))
    self.pause_play_state = True
    self.pause_play_btn.clicked.connect(self.pause_play)
    
    self.fw_track_btn = QPushButton(objectName = "fw_track_btn",
                                    icon = QIcon(r"ui\assets\fw_track.svg"), 
                                    flat = True, 
                                    size = QSize(self.height, self.height), 
                                    iconSize = QSize(self.height, self.height))
    
    self.loop_btn = QPushButton(objectName = "loop_btn",
                                icon = QIcon(r"ui\assets\loop.svg"), 
                                flat = True, 
                                size = QSize(self.height, self.height), 
                                iconSize = QSize(self.height, self.height))
    
    self.layout.addWidget(self.shuffle_btn)
    self.layout.addSpacing(self.height)
    self.layout.addWidget(self.bw_track_btn)
    self.layout.addWidget(self.pause_play_btn)
    self.layout.addWidget(self.fw_track_btn)
    self.layout.addSpacing(self.height)
    self.layout.addWidget(self.loop_btn)

  def pause_play(self):
    
    if self.pause_play_state == True:
      self.pause_play_btn.setIcon(QIcon(r"ui\assets\pause.svg"))
      self.pause_play_state = False
    else:
      self.pause_play_btn.setIcon(QIcon(r"ui\assets\play.svg"))
      self.pause_play_state = True

      
class SongInfo(QFrame):
  def __init__(self, parent) -> None:
    super().__init__(parent) 

    self.setObjectName("SongInfo")

    self.size = int(parent.parent.screen_size[0] * 0.01)

    self.layout = QGridLayout()
    self.setLayout(self.layout)

    self.art = QPushButton(objectName = "art",
                           icon = QIcon(r"ui\assets\placeholder.svg"),
                           flat = True,  
                           iconSize = QSize(self.size*2, self.size*2))
    self.art.setFixedSize(QSize(self.size*3, self.size*3))
    self.layout.addWidget(self.art, 0, 0)

    self.name_layout = QVBoxLayout()
    self.name_layout.setContentsMargins(5, 10, 0, 10)
    self.song_name = QLabel("Song Name", objectName = "song_name")
    self.artist_name = QLabel("Artist Name", objectName = "artist_name")

    self.name_layout.addWidget(self.song_name)
    self.name_layout.addWidget(self.artist_name)

    self.layout.addLayout(self.name_layout, 0, 1)


class ProgressBar(QFrame):
  def __init__(self, parent) -> None:
    super().__init__(parent)

    self.setObjectName("ProgressBar")

    self.setFixedWidth(int(parent.parent.screen_size[0] * 0.18))
    self.setFixedHeight(int(parent.parent.screen_size[0] * 0.005))

    self.layout = QHBoxLayout()
    self.layout.setContentsMargins(0, 0, 0, 0)
    self.setLayout(self.layout)

    self.bar = QSlider(Qt.Orientation.Horizontal, objectName="time_bar")
    self.bar.setRange(0, 100)
    self.layout.addWidget(self.bar)


class VolumeControls(QFrame):
  def __init__ (self, parent) -> None:
    super().__init__(parent)

    self.setObjectName("VolumeControls")

    self.volume_state = 2
    self.volume = 100

    self.layout = QHBoxLayout()
    self.layout.setContentsMargins(0, 0, 0, 0)
    self.setLayout(self.layout)

    self.btn_size = int(parent.parent.screen_size[0] * 0.02)
    self.mute_btn = QPushButton(objectName = "mute_btn",
                                   icon = QIcon(r"ui\assets\mute_off_2.svg"), 
                                   flat = True, 
                                   size = QSize(self.btn_size, self.btn_size), 
                                   iconSize = QSize(self.btn_size, 
                                                    self.btn_size))
    self.mute_btn.clicked.connect(self.mute_btn_pressed)
    self.mute_btn.state = False

    self.layout.addWidget(self.mute_btn)

    self.bar = QSlider(Qt.Orientation.Horizontal, objectName="volume_bar")
    self.bar.setRange(0, 100)
    self.bar.setValue(100)
    self.bar.setFixedHeight(int(self.btn_size / 3))
    self.bar.valueChanged.connect(self.volume_changed)

    self.layout.addWidget(self.bar)

  def mute_btn_pressed(self):
    if self.mute_btn.state:
      self.mute_btn.setIcon(QIcon(fr"ui\assets\mute_off_{self.volume_state}.svg"))
      self.mute_btn.state = False
      self.volume = self.bar.value()
      self.bar.setEnabled(True)
    else:
      self.mute_btn.setIcon(QIcon(r"ui\assets\mute_on.svg"))
      self.mute_btn.state = True
      self.bar.setEnabled(False)
      self.volume = 0

  def volume_changed(self):
    if self.bar.value() > 66:
      self.mute_btn.setIcon(QIcon(r"ui\assets\mute_off_2.svg"))
      self.volume_state = 2
    elif self.bar.value() > 33:
      self.mute_btn.setIcon(QIcon(r"ui\assets\mute_off_1.svg"))
      self.volume_state = 1
    else:
      self.mute_btn.setIcon(QIcon(r"ui\assets\mute_off_0.svg"))
      self.volume_state = 0
    
    self.volume = self.bar.value()
    print(self.volume)