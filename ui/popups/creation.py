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
    def __init__(self, window, name: str, desc: bool, controls: list) -> None:
        """Initialise a creation popup.

        Args:
            window (MainWindow): The window it a child of.
            name (str): The name of the popup window.
            desc (bool): Whether or not the desc should be displayed.
            controls (list): A list of control buttons to be added.
        """
        super().__init__()

        # Setup the layout.
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.icon = r"ui\assets\file.svg"
        self.name = name

        self.setModal(True) # Always on top

        # Link the widget to its style sheet.
        self.setObjectName("CreationPopup")
        self.setStyleSheet(open(r"ui\popups\stylesheets\creation.qss").read())

        self.setFixedWidth(int(window.get_screen_size()[0] / 4))

        self.contentLayout = QHBoxLayout()

        # Create the icon changer and link it to the change icon function
        self.icon_changer = QPushButton(objectName="icon_changer",
                                        icon=QIcon(self.icon),
                                        flat=True)
        self.icon_changer.pressed.connect(self.change_icon)
        self.contentLayout.addWidget(self.icon_changer, stretch=2)

        self.info_changer = InfoChanger(self, name, desc)
        self.contentLayout.addWidget(self.info_changer, stretch=3)

        self.controlsLayout = QHBoxLayout()

        # Add all of the controls which were passed on initialisation.
        for control in controls:
            btn = QPushButton(objectName="control", text=control[0])
            btn.clicked.connect(control[1])
            self.controlsLayout.addWidget(btn)

        self.layout.addLayout(self.contentLayout)
        self.layout.addSpacing(30)
        self.layout.addLayout(self.controlsLayout)

        self.layout.setContentsMargins(20, 20, 20, 20)

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setFocus()

    def change_icon(self):
        """Prompts the user with a file dialog for them to upload a playlist /
        song icon.
        """

        # Open the file dialog
        self.icon = Selector().get_file("image")

        # If a file was selected attempt to load the file as an image
        if self.icon[0] not in (None, '') and isinstance(self.icon[0], str):
            self.icon = self.icon[0]
            self.icon_changer.setIcon(QIcon(self.icon))
            self.icon_changer.setIconSize(QSize(self.icon_changer.width(),
                                                self.icon_changer.height()))
        else:
            self.icon = r"ui\assets\placeholder.svg"

    def resizeEvent(self, a0: QResizeEvent | None):
        """The function called when the popup is resized. It will never be
        called during runtime, but will be called twice as the popup is
        initialised.

        Args:
            a0 (QResizeEvent | None): Dummy param required by Qt.
        """
        self.icon_changer.setFixedSize(self.icon_changer.width(),
                                       self.icon_changer.width())
        self.icon_changer.setIconSize(QSize(int(self.icon_changer.width()*0.66),
                                            int(self.icon_changer.width()*0.66)))


class InfoChanger(QFrame):
    def __init__(self, parent: QDialog, name: str, desc: bool) -> None:
        """The initialisation function for the creation popups info changer.

        Args:
            parent (QDialog): The parent dialog box
            name (str): The placeholder name for the name field
            desc (bool): Should the description field be shown. 
        """
        super().__init__(parent)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Setup Name and Description edit panels.
        self.name_edit = QLineEdit(objectName="name",
                                   placeholderText=name)
        self.desc_edit = QLineEdit(objectName="desc",
                                   placeholderText="Description",
                                   alignment=Qt.AlignmentFlag.AlignTop)
        self.desc_edit.setSizePolicy(QSizePolicy.Policy.Expanding,
                                     QSizePolicy.Policy.Expanding)

        self.layout.addWidget(self.name_edit)

        # If the descripiton is enabled add it to the layout
        if desc:
            self.layout.addWidget(self.desc_edit)

    def resizeEvent(self, a0: QResizeEvent | None):
        """The function called when the info changer is resized. Used to scale
        font size correctly to fit the page. 

        Args:
            a0 (QResizeEvent | None): Dummy param required by Qt
        """

        # Get the font object being used for the name. 
        font = self.name_edit.font()

        # Set the name font size to 1/7 the dialog height
        font.setPointSize(int(self.height()/7))
        self.name_edit.setFont(font)

        # Set the description font size to 1/12 the font height
        font.setPointSize(int(self.height()/12))
        self.desc_edit.setFont(font)


class CreatePlaylist(CreationPopup):
    def __init__(self, window) -> None:
        """Instance of the Creation Popup which is setup to allow the user to
        create playlists.

        Args:
            window (QFrame): The parent window the popup will belong to.
        """
        super().__init__(window, "Playlist Name", True,
                         [("Save", self.save), ("Cancel", self.reject)])

    def save(self):
        """Formats the data of the playlist for it to be saved and then passes
        it to the file handler for saving. 
        """

        self.data = {
            "name": self.info_changer.name_edit.text(),
            "description": self.info_changer.desc_edit.text(),
            "icon": self.icon,
            "songs": []
        }

        CreatePlaylistFile(self.data)
        # Close the popup. 
        self.accept()


class UploadSong(CreationPopup):
    def __init__(self, window) -> None:
        """Instance of the Creation Popup setup to allow users to upload songs.

        Args:
            window (QFrame): The parent window the popup belongs too. 
        """
        super().__init__(window, "Song Name", False,
                         [("Save", self.save), ("Upload", self.upload_song),
                          ("Cancel", self.reject)])

        self.file = None

    def save(self):
        """Checks that their is a file to be saved and then passes it to the
        file handler.
        """
        if self.file:
            self.data["file"] = self.file
            CreateSongFile(self.data)
            self.accept()

    def upload_song(self):
        """Handles song uploads from the popup, requesting the songs data from
        shazam, and displaying it to the user. 
        """

        # Create a file dialog for the song to be selected. 
        self.file = Selector().get_file(type="song")[0]

        # Check if a song was uploaded. 
        if self.file:
            # Attempt to load the songs data, fails if their is no internet. 
            try:
                self.data = recognize_song.recognise(self.file)
                self.get_and_set_image_from_url(
                    self.data["images"]["coverart"])
                self.info_changer.name_edit.setText(self.data["title"])
            except:
                pass

    def get_and_set_image_from_url(self, image_url: str):
        """Attempts to get an image over HTTP and set it as the icon for the
        playlist.

        Args:
            image_url (str): The url of the image
        """

        # Create an HTTP request for the image
        request = requests.get(image_url)

        # Load the image as a pixmap
        pixmap = QPixmap()
        pixmap.loadFromData(request.content)

        # Convert the pixmap to an icon and set it. 
        icon = QIcon(pixmap)
        self.icon_changer.setIcon(icon)
        self.icon_changer.setIconSize(QSize(self.icon_changer.width(),
                                            self.icon_changer.height()))
