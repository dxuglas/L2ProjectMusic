from PyQt6.QtWidgets import (
  QFileDialog
)

IMAGE_EXTS = "*.jpg *.jpeg *.png *.webp *.svg"
SONG_EXTS = "*.mp3 *.wav *.ogg"

class Selector(QFileDialog):
  def __init__(self) -> None:
    super().__init__()

    self.setModal(True)
    self.setOption(QFileDialog.Option.ReadOnly, True)

  def get_file(self, type):
    if type == "image": ext = IMAGE_EXTS
    elif type == "song": ext = SONG_EXTS
    return self.getOpenFileName(filter=ext)

