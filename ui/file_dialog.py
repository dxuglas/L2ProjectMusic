from PyQt6.QtWidgets import (
  QFileDialog
)

IMAGE_EXTS = "*.jpg *.jpeg *.png *.webp *.svg"

class ArtSelector(QFileDialog):
  def __init__(self) -> None:
    super().__init__()

    self.setModal(True)
    self.setOption(QFileDialog.Option.ReadOnly, True)

  def get_file(self):
    return self.getOpenFileName(filter=IMAGE_EXTS)
