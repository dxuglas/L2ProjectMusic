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
  def __init__(self, parent) -> None:
    super().__init__()

    self.parent = parent

    self.setStyleSheet(open(r"ui\stylesheets\ui.qss").read())

    self.title_bar = TitleBar(self)
    self.setTitleBar(self.title_bar)

    self.screen_size = self.get_screen_size()
    self.setMinimumSize(int(self.screen_size[0]/2), 
                      int(self.screen_size[0]/2.82))
    self.setGeometry(int(self.screen_size[0] / 4), 
                         int((self.screen_size[1] - int(self.screen_size[0]/2.82))/2),
                         int(self.screen_size[0]/2), int(self.screen_size[0]/2.82))

    self.layout = QVBoxLayout()
    self.setLayout(self.layout)
    self.layout.setContentsMargins(0, self.titleBar.frameGeometry().height(), 0, 0)
    self.center_layout = QHBoxLayout()
    self.center_layout.setContentsMargins(0, 0, 0, 0)

    self.library = Library(self)
    self.center_layout.addWidget(self.library, 
                                 alignment= Qt.AlignmentFlag.AlignLeft)
    
    self.page_handler = PageHandler(self)
    self.center_layout.addWidget(self.page_handler)

    self.media_layout = QHBoxLayout()
    self.media_layout.setContentsMargins(0, 0, 0, 0)
    self.media_layout.addWidget(MediaInterface(self),
                          alignment=Qt.AlignmentFlag.AlignBottom)
    
    self.layout.addLayout(self.center_layout)
    self.layout.addLayout(self.media_layout)

  def get_screen_size(self):
    screen_size = self.parent.primaryScreen().size()
    
    return [screen_size.width(), screen_size.height()]
  
  def get_window_size(self):
    return [self.width(), self.height()]
  
  def resizeEvent(self, e):
    self.setStyleSheet(f"""WindowsFramelessWindow {{ background-color: 
                       qlineargradient(x1:0, y1:0, x2:1, y2:0, stop: 0 black, 
                       stop: {self.library.width / self.width()} black, 
                       stop: {self.library.width / self.width() * 1.021} white, 
                       stop: 1 white) }}""")
    return super().resizeEvent(e)
    
    
class TitleBar(QTitleBar):
  def __init__(self, parent) -> None:
    super().__init__(parent)
