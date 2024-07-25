from PyQt6.QtWidgets import (
  QFrame,
  QLineEdit,
  QHBoxLayout,
  QVBoxLayout,
  QPushButton,
  QDialog,
  QSizePolicy,
)
from PyQt6.QtGui import (
  QIcon,
  QResizeEvent,
  QPixmap
)
from PyQt6.QtCore import (
  Qt,
  QSize
)

import requests

from .file_dialog import Selector
from file_handler.save import CreatePlaylistFile, CreateSongFile
import shazam_interface.recognize_song as recognize_song


class CreationPopup(QDialog):
  def __init__(self, window, name: str, desc: bool, controls: list, ) -> None:
    super().__init__()
    self.layout = QVBoxLayout()
    self.setLayout(self.layout)
    
    self.icon = r"ui\assets\placeholder.svg"
    self.name = name

    self.setModal(True)
    self.setObjectName("CreationPopup")
    self.setStyleSheet(open(r"ui\popups\stylesheets\creation.qss").read())

    self.setFixedWidth(int(window.get_screen_size()[0] / 4))

    self.contentLayout = QHBoxLayout()

    self.icon_changer = QPushButton(objectName = "icon_changer",
                                    icon=QIcon(self.icon),
                                    flat=True)
    self.icon_changer.pressed.connect(self.change_icon)
    self.contentLayout.addWidget(self.icon_changer, stretch=2)
    
    self.info_changer = InfoChanger(self, name, desc)
    self.contentLayout.addWidget(self.info_changer, stretch=3)

    self.controlsLayout = QHBoxLayout()

    for control in controls:
      btn = QPushButton(objectName = "control", text = control[0])
      btn.clicked.connect(control[1])
      self.controlsLayout.addWidget(btn)


    self.layout.addLayout(self.contentLayout)
    self.layout.addSpacing(30)
    self.layout.addLayout(self.controlsLayout)

    self.layout.setContentsMargins(20, 20, 20, 20)

    self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
    self.setFocus()

  def change_icon(self):
    self.icon = Selector().get_file("image")
    
    if self.icon[0] not in (None, '') and isinstance(self.icon[0], str):
      self.icon = self.icon[0]
      self.icon_changer.setIcon(QIcon(self.icon))
      self.icon_changer.setIconSize(QSize(self.icon_changer.width(), 
                                          self.icon_changer.height()))
    else:
      self.icon = r"ui\assets\placeholder.svg"

  def resizeEvent(self, a0: QResizeEvent | None):
    self.icon_changer.setFixedSize(self.icon_changer.width(), 
                                   self.icon_changer.width())
    self.icon_changer.setIconSize(QSize(int(self.icon_changer.width()*0.66), 
                                        int(self.icon_changer.width()*0.66)))


class InfoChanger(QFrame):
  def __init__(self, parent, name, desc) -> None:
    super().__init__(parent)

    self.layout = QVBoxLayout()
    self.setLayout(self.layout)

    self.name_edit = QLineEdit(objectName = "name", 
                               placeholderText = name)
    self.desc_edit = QLineEdit(objectName = "desc",
                               placeholderText = "Description",
                               alignment = Qt.AlignmentFlag.AlignTop)
    self.desc_edit.setSizePolicy(QSizePolicy.Policy.Expanding,
                                 QSizePolicy.Policy.Expanding)

    self.layout.addWidget(self.name_edit)
    if desc: self.layout.addWidget(self.desc_edit)

  def resizeEvent(self, a0: QResizeEvent | None):

    font = self.name_edit.font()

    font.setPointSize(int(self.height()/7))
    self.name_edit.setFont(font)

    font.setPointSize(int(self.height()/12))
    self.desc_edit.setFont(font)


class CreatePlaylist(CreationPopup):
  def __init__(self, window) -> None:
    super().__init__(window, "Playlist Name", True, 
                     [("Save", self.save), ("Cancel", self.reject)])

  def save(self):

    self.data = {
      "name" : self.info_changer.name_edit.text(),
      "description" : self.info_changer.desc_edit.text(),
      "icon": self.icon
    }

    CreatePlaylistFile(self.data)
    self.accept()

class UploadSong(CreationPopup):
  def __init__(self, window) -> None:
    super().__init__(window, "Song Name", False, 
                     [("Save", self.save), ("Upload", self.upload_song), 
                      ("Cancel", self.reject)])
    
    self.file = None
    
  def save(self):
    if self.file:
      CreateSongFile(self.data)
      self.accept()

  def upload_song(self):
    self.file = Selector().get_file(type="song")[0]

    if self.file:
      try:
        self.data = recognize_song.recognise(self.file)
        self.get_and_set_image_from_url(self.data["images"]["coverart"])
        self.info_changer.name_edit.setText(self.data["title"])
      except:
        pass

  def get_and_set_image_from_url(self, image_url):
    request = requests.get(image_url)

    pixmap = QPixmap()
    pixmap.loadFromData(request.content)

    icon = QIcon(pixmap)
    self.icon_changer.setIcon(icon)
    self.icon_changer.setIconSize(QSize(self.icon_changer.width(), 
                                        self.icon_changer.height()))

