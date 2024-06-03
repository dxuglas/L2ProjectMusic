from PyQt6.QtWidgets import (
  QFrame, 
  QHBoxLayout,
  QVBoxLayout,
  QPushButton,
  QLabel,
  QScrollArea
)
from PyQt6.QtCore import (
  QSize,
  Qt
)
from PyQt6.QtGui import (
  QIcon
)

class PlaylistPage(QFrame):
  def __init__(self, parent):
    super().__init__(parent)
    self.size_parent = parent.parent

    self.setStyleSheet(open(r"ui\stylesheets\playlist.qss").read())

    self.layout = QVBoxLayout()
    self.setLayout(self.layout)

    self.layout.addWidget(InfoPanel(self))
    self.layout.addWidget(SongSelector(self))


class InfoPanel(QFrame):
  def __init__(self, parent):
    super().__init__(parent)
    self.size_parent = parent.size_parent

    self.layout = QHBoxLayout()
    self.setLayout(self.layout)

    self.size = int(self.size_parent.screen_size[0] * 0.04)
  
    self.cover = QPushButton(objectName = "cover",
                             icon = QIcon(r"ui\assets\placeholder.svg"),
                             flat = True,  
                             iconSize = QSize(self.size*2, self.size*2))
    self.cover.setFixedSize(QSize(self.size*3, self.size*3))
    self.layout.addWidget(self.cover)

    self.layout.addSpacing(int(self.size/8))

    self.name = QLabel("Playlist Name #1", objectName = "name")
    self.font = self.name.font()
    self.font.setPointSize(int(self.size*0.5))
    self.name.setFont(self.font)
    self.layout.addWidget(self.name)


class SongSelector(QFrame):
  def __init__(self, parent):
    super().__init__(parent)
    self.size_parent = parent.size_parent

    self.setObjectName("SongSelector")

    self.layout = QVBoxLayout()
    self.setLayout(self.layout)

    self.scroll_area = QFrame(objectName = "scroll_area")
    self.scroll_area.layout = QVBoxLayout()
    self.scroll_area.setLayout(self.scroll_area.layout)

    for i in range(8):
      self.scroll_area.layout.addWidget(SongPanel(self))

    self.scroller = QScrollArea(objectName="scroller",
                                widgetResizable=True,
                                verticalScrollBarPolicy=Qt.ScrollBarPolicy.ScrollBarAlwaysOn,
                                horizontalScrollBarPolicy=Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    self.scroller.setWidget(self.scroll_area)
    self.layout.addWidget(self.scroller)


class SongPanel(QFrame):
  def __init__(self, parent):
    super().__init__(parent)
    self.size_parent = parent.size_parent

    self.setObjectName("SongPanel")

    self.layout = QHBoxLayout()
    self.setLayout(self.layout)

    self.size = int(self.size_parent.screen_size[0] * 0.005)

    self.art = QPushButton(objectName = "art",
                           icon = QIcon(r"ui\assets\placeholder.svg"),
                           flat = True,  
                           iconSize = QSize(self.size*2, self.size*2))
    self.art.setFixedSize(QSize(self.size*3, self.size*3))
    self.layout.addWidget(self.art)

    