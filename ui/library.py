from PyQt6.QtWidgets import (
  QFrame, 
  QPushButton,
  QVBoxLayout,
  QLabel 
)
from PyQt6.QtCore import (
  QSize,
  Qt
)
from PyQt6.QtGui import QIcon

class Library(QFrame):
  def __init__(self, parent) -> None:
    super().__init__(parent)
    self.parent = parent

    self.setObjectName("Library")
    self.setStyleSheet(open(r"ui\stylesheets\library.qss").read())
    
    self.width = int(self.parent.screen_size[0]*0.066)
    self.setFixedWidth(self.width)
    self.setMinimumHeight(int(self.parent.screen_size[0]/2.774))

    self.layout = QVBoxLayout()
    self.layout.setContentsMargins(0, 0, 0, 0)
    self.setLayout(self.layout)

    #self.layout.addWidget(MenuContainer(self), 
    #                      alignment=Qt.AlignmentFlag.AlignTop)
    
    #self.lib_label = QLabel("LIBRARY", objectName = "lib_label")
    #self.layout.addWidget(self.lib_label, alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

class MenuContainer(QFrame):
  def __init__(self, parent) -> None:
    super().__init__(parent)

    self.size = int(parent.parent.screen_size[0] * 0.027)
    self.wmargins = int(parent.parent.screen_size[0] * 0.012)

    self.layout = QVBoxLayout()
    #self.layout.setContentsMargins(self.wmargins, 
     #                              int(parent.parent.screen_size[0]*0.006), 
    #                               self.wmargins, 0)
    self.setLayout(self.layout)

    self.home_btn = QPushButton(objectName = "home_btn",
                                icon = QIcon(r"ui\assets\home.svg"),
                                flat = True, 
                                size = QSize(self.size, self.size), 
                                iconSize = QSize(self.size, self.size))
    self.search_btn = QPushButton(objectName = "search_btn",
                                  icon = QIcon(r"ui\assets\search.svg"),
                                  flat = True, 
                                  size = QSize(self.size, self.size), 
                                  iconSize = QSize(self.size, self.size))
    
    self.layout.addWidget(self.home_btn)
    self.layout.addWidget(self.search_btn)