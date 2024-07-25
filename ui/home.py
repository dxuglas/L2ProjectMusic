from PyQt6.QtWidgets import (
  QFrame,
  QVBoxLayout,
  QGridLayout
)


class HomePage(QFrame):
  def __init__(self, parent) -> None:
    super().__init__(parent)

    self.setObjectName("HomePage")
    self.setStyleSheet(open(r"ui\stylesheets\home.qss").read())

    self.layout = QVBoxLayout()
    self.layout.setContentsMargins(10, 10, 10, 10)
    self.setLayout(self.layout)


class ReccomendationPanel(QFrame):
  def __init__(self, parent) -> None:
    super().__init__(parent)

    self.setObjectName("ReccomendationPanel")

    self.layout = QGridLayout
    self.layout.setContentsMargins(10, 10, 10, 10)
    self.setLayout(self.layout)

  
