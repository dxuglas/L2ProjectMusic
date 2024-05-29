from PyQt6.QtWidgets import (
  QFrame, 
  QHBoxLayout,
  QVBoxLayout,
  QPushButton
)
from PyQt6.QtCore import (
  QSize
)
from PyQt6.QtGui import (
  QIcon,
)

class PlaylistPage(QFrame):
  def __init__(self, parent):
    super().__init__(parent)
    self.parent = parent

    self.setStyleSheet(open(r"ui\stylesheets\playlist.qss").read())

    self.layout = QVBoxLayout()
    self.setLayout(self.layout)

    self.layout.addWidget(InfoPanel(self))


class InfoPanel(QFrame):
  def __init__(self, parent):
    super().__init__(parent)

    self.layout = QHBoxLayout()
    self.setLayout(self.layout)

    self.size = int(parent.parent.parent.screen_size[0] * 0.04)
  
    self.cover = QPushButton(objectName = "cover",
                             icon = QIcon(r"ui\assets\placeholder.svg"),
                             flat = False, 
                             size = QSize(self.size * 2, self.size * 2), 
                             iconSize = QSize(self.size, self.size))
    self.cover.setFixedSize(QSize(self.size*2, self.size*2))
    
    self.layout.addWidget(self.cover)

