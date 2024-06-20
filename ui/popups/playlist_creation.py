from PyQt6.QtWidgets import (
  QFrame,
  QLineEdit,
  QHBoxLayout,
  QVBoxLayout,
  QPushButton,
  QDialog,
  QSizePolicy
)

from PyQt6.QtGui import (
  QIcon
)

from PyQt6.QtCore import (
  Qt,
  QSize
)

from ..file_dialog import ArtSelector, IMAGE_EXTS


class CreationPopup(QDialog):
  def __init__(self) -> None:
    super().__init__()
    self.layout = QVBoxLayout()
    self.setLayout(self.layout)

    self.setModal(True)
    self.setObjectName("CreationPopup")
    self.setStyleSheet(open(r"ui\popups\stylesheets\playlist_creation.qss").read())

    self.contentLayout = QHBoxLayout()

    self.icon_changer = QPushButton(objectName = "icon_changer",
                                    icon=QIcon(r"ui\assets\placeholder.svg"),
                                    flat=True, iconSize = QSize(66, 66))
    self.icon_changer.setFixedSize(100, 100)
    self.icon_changer.pressed.connect(self.change_icon)
    self.contentLayout.addWidget(self.icon_changer)
    
    self.info_changer = InfoChanger(self)
    self.contentLayout.addWidget(self.info_changer)

    self.controlsLayout = QHBoxLayout()

    self.save_btn = QPushButton(objectName = "control", text="save")
    self.controlsLayout.addWidget(self.save_btn)
    self.save_btn.clicked.connect(self.accept)

    self.cancel_btn = QPushButton(objectName = "control", text="cancel")
    self.controlsLayout.addWidget(self.cancel_btn)
    self.cancel_btn.clicked.connect(self.reject)

    self.layout.addLayout(self.contentLayout)
    self.layout.addLayout(self.controlsLayout)

    self.layout.setContentsMargins(10, 20, 10, 20)

    self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

  def change_icon(self):
    file = ArtSelector.getOpenFileName(filter=IMAGE_EXTS)
    
    if file[0] not in (None, ''):
      self.icon = file[0]
      self.icon_changer.setIcon(QIcon(self.icon))
      self.icon_changer.setIconSize(QSize(100, 100))


class InfoChanger(QFrame):
  def __init__(self, parent) -> None:
    super().__init__(parent)

    self.layout = QVBoxLayout()
    self.setLayout(self.layout)
    self.layout.setContentsMargins(0, 0, 0, 0)

    self.name_edit = QLineEdit(placeholderText = "Playlist Name")
    self.desc_edit = QLineEdit(placeholderText = "Playlist Description",
                               alignment = Qt.AlignmentFlag.AlignTop)
    self.desc_edit.setSizePolicy(QSizePolicy.Policy.Expanding,
                                 QSizePolicy.Policy.Expanding)

    self.layout.addWidget(self.name_edit)
    self.layout.addWidget(self.desc_edit)

