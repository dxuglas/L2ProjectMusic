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

from ..file_dialog import ArtSelector
from file_handler.save import CreatePlaylistFile 


class CreationPopup(QDialog):
  def __init__(self) -> None:
    super().__init__()
    self.layout = QVBoxLayout()
    self.setLayout(self.layout)
    
    self.icon = r"ui\assets\placeholder.svg"
    self.setModal(True)
    self.setObjectName("CreationPopup")
    self.setStyleSheet(open(r"ui\popups\stylesheets\playlist_creation.qss").read())

    self.contentLayout = QHBoxLayout()

    self.icon_changer = QPushButton(objectName = "icon_changer",
                                    icon=QIcon(self.icon),
                                    flat=True, iconSize = QSize(66, 66))
    self.icon_changer.setFixedSize(200, 200)
    self.icon_changer.pressed.connect(self.change_icon)
    self.contentLayout.addWidget(self.icon_changer)
    
    self.info_changer = InfoChanger(self)
    self.contentLayout.addWidget(self.info_changer)

    self.controlsLayout = QHBoxLayout()

    self.save_btn = QPushButton(objectName = "control", text="Save")
    self.save_btn.setFixedSize(QSize(50, 20))
    self.controlsLayout.addWidget(self.save_btn, alignment=Qt.AlignmentFlag.AlignLeft)
    self.save_btn.clicked.connect(self.save)

    self.cancel_btn = QPushButton(objectName = "control", text="Cancel")
    self.cancel_btn.setFixedSize(QSize(65, 20))
    self.controlsLayout.addWidget(self.cancel_btn, alignment=Qt.AlignmentFlag.AlignRight)
    self.cancel_btn.clicked.connect(self.reject)

    self.layout.addLayout(self.contentLayout)
    self.layout.addSpacing(30)
    self.layout.addLayout(self.controlsLayout)

    self.layout.setContentsMargins(30, 30, 30, 30)

    self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

  def change_icon(self):
    self.icon = ArtSelector().get_file()
    
    if self.icon[0] not in (None, ''):
      self.icon = self.icon[0]
      self.icon_changer.setIcon(QIcon(self.icon))
      self.icon_changer.setIconSize(QSize(200, 200))

  def save(self):
    self.data = {}
    self.data["name"] = self.info_changer.name_edit.text()
    self.data["description"] = self.info_changer.desc_edit.text()
    self.data["icon"] = self.icon

    CreatePlaylistFile(self.data)
    self.accept()


class InfoChanger(QFrame):
  def __init__(self, parent) -> None:
    super().__init__(parent)

    self.layout = QVBoxLayout()
    self.setLayout(self.layout)

    self.name_edit = QLineEdit(objectName = "name", 
                               placeholderText = "Playlist Name")
    self.desc_edit = QLineEdit(objectName = "desc",
                               placeholderText = "Description",
                               alignment = Qt.AlignmentFlag.AlignTop)
    self.desc_edit.setSizePolicy(QSizePolicy.Policy.Expanding,
                                 QSizePolicy.Policy.Expanding)

    self.layout.addWidget(self.name_edit)
    self.layout.addWidget(self.desc_edit)

