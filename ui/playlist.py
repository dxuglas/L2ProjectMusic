from PyQt6.QtWidgets import (
  QFrame, 
  QHBoxLayout,
  QVBoxLayout,
  QGridLayout,
  QPushButton,
  QLabel,
  QScrollArea,
  QSizePolicy
)
from PyQt6.QtCore import (
  QSize,
  Qt
)
from PyQt6.QtGui import (
  QIcon,
  QResizeEvent
)

class PlaylistPage(QFrame):
  def __init__(self, parent) -> None:
    super().__init__(parent)
    self.size_parent = parent.parent

    self.setObjectName("PlaylistPage")
    self.setStyleSheet(open(r"ui\stylesheets\playlist.qss").read())

    self.layout = QVBoxLayout()
    self.setLayout(self.layout)

    self.info = InfoPanel(self)
    self.selector = SongSelector(self)
    self.layout.addWidget(self.info)
    self.layout.addWidget(self.selector)

    self.layout.setContentsMargins(10, 10, 10, 0)
  
  def resizeEvent(self, a0: QResizeEvent | None) -> None:
    self.setFixedHeight(int(self.size_parent.get_window_size()[1] - 100))
    self.selector.resizeEvent(a0)
    return super().resizeEvent(a0)


class InfoPanel(QFrame):
  def __init__(self, parent) -> None:
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
    self.layout.setContentsMargins(0, 0, 0, 0)
    self.layout.addSpacing(int(self.size/8))

    self.name = QLabel("Playlist Name #1", objectName = "playlist_name")
    self.font = self.name.font()
    self.font.setPointSize(int(self.size*0.5))
    self.name.setFont(self.font)
    self.layout.addWidget(self.name)

  def resizeEvent(self, a0: QResizeEvent | None) -> None:
    self.setFixedHeight(self.height())
    return super().resizeEvent(a0)


class SongSelector(QScrollArea):
  def __init__(self, parent) -> None:
    super().__init__(parent)
    self.parent = parent
    self.size_parent = parent.size_parent
    self.setObjectName("SongSelector")

    self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

    self.width = int(self.size_parent.screen_size[0] / 2.3)-30
    self.setMinimumWidth(self.width)

    self.scroll_area = QFrame(objectName = "scroll_area")

    self.layout = QVBoxLayout()
    self.scroll_area.setLayout(self.layout)
    self.layout.setContentsMargins(0, 0, 10, 0)

    for i in range(14):
      self.layout.addWidget(SongPanel(self))

    self.setWidget(self.scroll_area)

  def resizeEvent(self, a0: QResizeEvent | None) -> None:
    self.setFixedHeight(int((self.parent.height() - self.parent.info.height()) * 0.85))
    print(self.height())
    return super().resizeEvent(a0)


class SongPanel(QFrame):
  def __init__(self, parent) -> None:
    super().__init__(parent)
    self.size_parent = parent.size_parent

    self.setObjectName("SongPanel")

    self.layout = QGridLayout()
    self.setLayout(self.layout)

    self.size = int(self.size_parent.screen_size[0] * 0.008)
    self.width = int(self.size_parent.screen_size[0] / 2.3-50)
    self.setMinimumWidth(self.width)

    self.art = QPushButton(objectName = "art",
                           icon = QIcon(r"ui\assets\placeholder.svg"),
                           flat = True,  
                           iconSize = QSize(self.size*2, self.size*2))
    self.art.setFixedSize(QSize(self.size*3, self.size*3))
    self.layout.addWidget(self.art, 0, 0)

    self.name_layout = QVBoxLayout()
    self.song_name = QLabel("Song Name", objectName = "song_name")
    self.artist_name = QLabel("Artist Name", objectName = "artist_name")

    self.name_layout.addWidget(self.song_name)
    self.name_layout.addWidget(self.artist_name)

    self.layout.addLayout(self.name_layout, 0, 1)

    self.album_name = QLabel("Album Name", objectName = "album_name")
    self.song_length = QLabel("0:00", objectName = "song_length")
    
    self.layout.addWidget(self.album_name, 0, 2, 
                          alignment=Qt.AlignmentFlag.AlignCenter)
    self.layout.addWidget(self.song_length, 0, 3, 
                          alignment=Qt.AlignmentFlag.AlignRight)
