from PyQt6.QtWidgets import QFrame, QPushButton
from PyQt6.QtCore import QSize


class MediaInterface(QFrame):
  def __init__(self, parent) -> None:
    super().__init__(parent)
    self.parent = parent

    self.setObjectName("MediaInterface")
    self.setStyleSheet(open(r"ui\stylesheets\media_interface.qss").read())

    self.setFixedHeight(int(self.parent.screen_size[0] * 0.039))


class MediaControls(QFrame):
  def __init__(self, parent) -> None:
    super().__init__(parent)

    self.setObjectName("MediaControls")

    self.pause_play_btn = QPushButton(objectName = "pause_play_btn",
                                      icon = ???, flat = True, size = QSize(???), iconSize = QSize(???))