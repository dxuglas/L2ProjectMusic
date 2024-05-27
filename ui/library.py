from PyQt6.QtWidgets import QFrame

class Library(QFrame):
  def __init__(self, parent) -> None:
    super().__init__(parent)
    self.parent = parent

    self.setObjectName("Library")
    self.setStyleSheet(open(r"ui\stylesheets\library.qss").read())
    
    self.width = int(self.parent.screen_size[0]*0.046)
    self.setFixedWidth(self.width)
    self.setMinimumHeight(int(self.parent.screen_size[0]*2.774))