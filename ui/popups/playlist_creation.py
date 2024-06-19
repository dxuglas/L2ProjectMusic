from PyQt6.QtWidgets import (
  QFrame,
  QLineEdit,
  QHBoxLayout,
  QVBoxLayout,
  QPushButton,
  QDialog,
  QFileDialog
)

from PyQt6.QtGui import (
  QIcon
)

from PyQt6.QtCore import (
  Qt,
  QSize
)


class CreationPopup(QDialog):
  def __init__(self) -> None:
    super().__init__()
    self.layout = QHBoxLayout()
    self.setLayout(self.layout)

    self.setModal(True)

    self.art_changer = ArtChanger(self)
    self.layout.addWidget(self.art_changer)
    
    self.info_changer = InfoChanger(self)
    self.layout.addWidget(self.info_changer)

    self.close_btn = QPushButton(text="close")
    self.layout.addWidget(self.close_btn)
    self.close_btn.clicked.connect(self.close_dialog)

    self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

  def close_dialog(self):
    self.accept()


class ArtChanger(QPushButton):
  def __init__(self, parent) -> None:
    super().__init__(parent)
    
    self.setFixedSize(100, 100)
    self.setIcon(QIcon(r"ui\assets\placeholder.svg"))
    self.setIconSize(QSize(66, 66))

    self.clicked.connect(self.file_selector)

  def file_selector(self):
    self.selector = QFileDialog()
    self.selector.show()


class InfoChanger(QFrame):
  def __init__(self, parent) -> None:
    super().__init__(parent)

    self.name_edit = QLineEdit()
    self.desc_edit = QLineEdit()

    self.layout = QVBoxLayout()
    self.setLayout(self.layout)

    self.layout.addWidget(self.name_edit)
    self.layout.addWidget(self.desc_edit)

