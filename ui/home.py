from PyQt6.QtWidgets import (
  QFrame,
  QVBoxLayout,
  QGridLayout
)

from media_handler.song_recomendations import SongRecomendations


class HomePage(QFrame):
  def __init__(self, parent) -> None:
    super().__init__(parent)

    self.setObjectName("HomePage")
    self.setStyleSheet(open(r"ui\stylesheets\home.qss").read())

    self.layout = QVBoxLayout()
    self.layout.setContentsMargins(10, 10, 10, 10)
    self.setLayout(self.layout)

    self.recommendation_panel = RecomendationPanel(self)


class RecomendationPanel(QFrame):
  def __init__(self, parent) -> None:
    super().__init__(parent)

    self.setObjectName("ReccomendationPanel")

    self.layout = QGridLayout()
    self.layout.setContentsMargins(10, 10, 10, 10)
    self.setLayout(self.layout)

    self.songs = SongRecomendations().from_library(4)
    print(self.songs)

  
