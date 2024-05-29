from qframelesswindow import (
  FramelessWindow as QWindow, 
  TitleBar as QTitleBar
)
from PyQt6.QtWidgets import (
  QVBoxLayout,
  QHBoxLayout
)
from PyQt6.QtCore import Qt

from .media_interface import MediaInterface
from .library import Library
from .page import PageHandler


class MainWindow(QWindow):
  def __init__(self, parent):
    super().__init__()

    self.parent = parent

    self.setStyleSheet(open(r"ui\stylesheets\ui.qss").read())

    self.title_bar = TitleBar(self)
    self.setTitleBar(self.title_bar)

    self.screen_size = self.get_screen_size()
    self.setMinimumSize(int(self.screen_size[0]/2), 
                      int(self.screen_size[0]/2.82))
    self.move(int(self.screen_size[0] / 4), 
              int((self.screen_size[1] - int(self.screen_size[0]/2.82))/2))
    
    self.layout = QVBoxLayout()
    self.setLayout(self.layout)
    self.layout.setContentsMargins(0, self.titleBar.frameGeometry().height(), 0, 0)

    self.center_layout = QHBoxLayout()
    self.center_layout.setContentsMargins(0, 0, 0, 0)
    self.center_layout.addWidget(Library(self), alignment= Qt.AlignmentFlag.AlignLeft)
    self.center_layout.addWidget(PageHandler(self))

    self.media_layout = QHBoxLayout()
    self.media_layout.setContentsMargins(0, 0, 0, 0)
    self.media_layout.addWidget(MediaInterface(self),
                          alignment=Qt.AlignmentFlag.AlignBottom)
    
    self.layout.addLayout(self.center_layout)
    self.layout.addLayout(self.media_layout)

  def get_screen_size(self):
    screen_size = self.parent.primaryScreen().size()
    
    return [screen_size.width(), screen_size.height()]
    
    
class TitleBar(QTitleBar):
  def __init__(self, parent):
    super().__init__(parent)
