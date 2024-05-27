from qframelesswindow import (
  FramelessWindow as QWindow, 
  TitleBar as QTitleBar
)
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtCore import Qt

from .media_interface import MediaInterface
from .library import Library


class MainWindow(QWindow):
  def __init__(self, parent):
    super().__init__()

    self.parent = parent

    self.setTitleBar(TitleBar(self))

    self.screen_size = self.get_screen_size()
    self.setMinimumSize(int(self.screen_size[0]/2), 
                      int(self.screen_size[0]/2.82))
    self.move(int(self.screen_size[0] / 4), 
              int((self.screen_size[1] - int(self.screen_size[0]/2.82))/2))
    
    self.layout = QVBoxLayout()
    self.setLayout(self.layout)
    self.layout.setContentsMargins(0, 0, 0, 0)
    self.layout.addWidget(Library(self), alignment=Qt.AlignmentFlag.AlignLeft)
    self.layout.addWidget(MediaInterface(self),
                          alignment=Qt.AlignmentFlag.AlignBottom)

  def get_screen_size(self):
    screen_size = self.parent.primaryScreen().size()
    
    return [screen_size.width(), screen_size.height()]
    
    
class TitleBar(QTitleBar):
  def __init__(self, parent):
    super().__init__(parent)