from PyQt6.QtWidgets import QFrame, QPushButton, QHBoxLayout, QVBoxLayout, QSlider
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon


class MediaInterface(QFrame):
  def __init__(self, parent) -> None:
    super().__init__(parent)
    self.parent = parent
    
    self.setObjectName("MediaInterface")
    self.setStyleSheet(open(r"ui\stylesheets\media_interface.qss").read())

    self.setFixedHeight(int(self.parent.screen_size[0] * 0.046))

    self.layout = QVBoxLayout()
    self.layout.setContentsMargins(0, int(self.parent.screen_size[0] * 0.007), 0, int(self.parent.screen_size[0] * 0.007))
    self.setLayout(self.layout)

    self.layout.addWidget(MediaControls(self), alignment = Qt.AlignmentFlag.AlignCenter)
    self.layout.addWidget(ProgressBar(self), alignment = Qt.AlignmentFlag.AlignCenter)


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
                                      iconSize = QSize(self.height, self.height))
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

      
class ProgressBar(QFrame):
  def __init__(self, parent) -> None:
    super().__init__(parent)

    self.setObjectName("ProgressBar")

    self.setFixedWidth(int(parent.parent.screen_size[0] * 0.18))
    self.setFixedHeight(int(parent.parent.screen_size[0] * 0.005))

    self.layout = QHBoxLayout()
    self.layout.setContentsMargins(0, 0, 0, 0)
    self.setLayout(self.layout)

    self.bar = QSlider(Qt.Orientation.Horizontal, objectName="bar")
    self.bar.setRange(0, 100)
    self.layout.addWidget(self.bar)