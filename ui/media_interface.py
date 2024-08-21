from PyQt6.QtWidgets import (
    QFrame,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QGridLayout,
    QSlider,
    QLabel,
    QSizePolicy
)
from PyQt6.QtCore import (
    QSize,
    Qt
)
from PyQt6.QtGui import QIcon, QResizeEvent


class MediaInterface(QFrame):
    def __init__(self, parent, song=None) -> None:
        """The Media Interface allows for the user to interact with the media
        controller, such as pausing, playing, skipping tracks, and adjusting
        the volume. 

        Args:
            parent (MainWindow): The window the media interface belongs to.
            song (LoadSong, optional): The current song. Defaults to None.
        """
        super().__init__(parent)
        self.parent = parent
        self.song = song
        self.controls = self.window().controls

        # Link widget to its stylesheet.
        self.setObjectName("MediaInterface")
        self.setStyleSheet(open(r"ui\stylesheets\media_interface.qss").read())

        # Set the widgets height based on the screen size.
        self.height = (int(self.parent.screen_size[0]*0.05))
        self.setFixedHeight(self.height)

        # Create the layout for the interface.
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        # The panel which displays ifno on the currently playing song.
        self.playing_info = PlayingInfo(self)
        self.layout.addWidget(self.playing_info,
                              alignment=Qt.AlignmentFlag.AlignLeft,
                              stretch=7)

        # The media control buttons.
        self.media_controls = MediaControls(self)
        self.layout.addWidget(self.media_controls, stretch=3)

        # The volume controls.
        self.volume_controls = VolumeControls(self)
        self.layout.addWidget(self.volume_controls, stretch=7)

    def load(self, song):
        """Load the currently playing song to the media interface. 

        Args:
            song (LoadSong): The currently playing song. 
        """

        self.playing_info.song = song
        # Update the playing info panel.
        self.playing_info.load()
        # Update the paused state of the media controls.
        self.media_controls.paused = True
        self.media_controls.pause_play_btn_pressed()


class PlayingInfo(QFrame):
    def __init__(self, parent, song=None) -> None:
        """Displays information about the currently playing song.

        Args:
            parent (QFrame): The parent of the panel
            song (LoadSong, optional): Song data. Defaults to None.
        """
        super().__init__(parent)
        self.song = song

        # Link panel to stylesheet.
        self.setObjectName("PlayingInfo")

        # Setup the panels layout with 0 margins around the outside.
        self.layout = QHBoxLayout()
        self.layout.setSpacing(3)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        # The song art display.
        self.art = PlayingArt(self, song)

        # Create the text layout
        self.text_layout = QVBoxLayout()
        self.text_layout.setSpacing(0)
        self.text_layout.setContentsMargins(7, 7, 7, 7)

        # Create the text labels.
        self.name = QLabel(objectName="name")
        self.artist = QLabel(objectName="artist")

        # Add the labels to the text layout.
        self.text_layout.addWidget(self.name)
        self.text_layout.addWidget(self.artist)

        # If their is a song load it otherwise set the default values.
        if self.song:
            self.load()
        else:
            self.art.setIcon(QIcon(r"ui\assets\placeholder.svg"))
            self.name.setText("Song Name")
            self.artist.setText("Artist Name")

        # Add the child widgets to the layout.
        self.layout.addWidget(self.art)
        self.layout.addLayout(self.text_layout)

    def load(self):
        """Updates the child widgets to display the current song information. 
        """
        self.art.setIcon(self.song.icon)
        self.art.resizeEvent(None)
        self.name.setText(self.song.name)
        self.artist.setText(self.song.artist)


class PlayingArt(QPushButton):
    def __init__(self, parent):
        """Displays the art of the currently playing song. 

        Args:
            parent (QFrame): The parent of the art display.
        """
        super().__init__(parent)
        self.parent = parent

        self.setObjectName("PlayingArt")
        self.setFlat(True)

    def resizeEvent(self, a0: QResizeEvent | None) -> None:
        """The function called when the art is resized. 

        Args:
            a0 (QResizeEvent | None): Dummy param required by Qt.
        """
        self.setFixedSize(QSize(self.parent.height(), self.parent.height()))

        # Change the icon scaling for if the default icon is used.
        if self.song:
            self.setIconSize(QSize(self.width(), self.height()))
        else:
            self.setIconSize(QSize(int(self.width()/2), int(self.height()/2)))


class MediaControls(QFrame):
    def __init__(self, parent: QFrame):
        """The controls which allow the user to interact with the media
        controller. 

        Args:
            parent (QFrame): The parent widget for the controls.
        """

        super().__init__(parent)
        self.parent = parent
        self.paused = True

        # Link the controls to their stylesheet.
        self.setObjectName("MediaControls")

        # Setup the layout
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        # Create control buttons and connect to call functions.
        self.track_back_btn = QPushButton(objectName="track_back_btn",
                                          flat=True,
                                          icon=QIcon(r"ui\assets\bw_track.svg"))
        self.track_back_btn.clicked.connect(self.parent.controls.play_last)

        self.pause_play_btn = QPushButton(objectName="pause_play_btn",
                                          flat=True,
                                          icon=QIcon(r"ui\assets\play.svg"))
        self.pause_play_btn.clicked.connect(self.pause_play_btn_pressed)

        self.track_fwd_btn = QPushButton(objectName="track_forward_btn",
                                         flat=True,
                                         icon=QIcon(r"ui\assets\fw_track.svg"))
        self.track_fwd_btn.clicked.connect(self.parent.controls.play_next)

        # Add the controls to the layout.
        self.layout.addWidget(self.track_back_btn)
        self.layout.addWidget(self.pause_play_btn)
        self.layout.addWidget(self.track_fwd_btn)

    def pause_play_btn_pressed(self):
        """Toggle the pause/play state of the media controller when the button
        is pressed. Also updates the button to show what the current state is. 
        """
        if self.paused:
            self.pause_play_btn.setIcon(QIcon(r"ui\assets\pause.svg"))
            self.paused = False
            self.parent.controls.play()
        else:
            self.pause_play_btn.setIcon(QIcon(r"ui\assets\play.svg"))
            self.paused = True
            self.parent.controls.pause()

    def resizeEvent(self, a0: QResizeEvent | None) -> None:
        """The function called when the media controls are resized. Enforces
        sizes for the button icons aswell as overall widget size.

        Args:
            a0 (QResizeEvent | None): Dummy param required by Qt. 
        """

        self.setFixedWidth(self.width())
        self.track_back_btn.setFixedHeight(self.track_back_btn.width())
        self.pause_play_btn.setFixedHeight(self.pause_play_btn.width())

        self.track_back_btn.setIconSize(QSize(self.track_back_btn.width(),
                                              self.track_back_btn.width()))
        self.pause_play_btn.setIconSize(QSize(self.pause_play_btn.width(),
                                              self.pause_play_btn.width()))
        self.track_fwd_btn.setIconSize(QSize(self.track_fwdrd_btn.width(),
                                             self.track_fwd_btn.width()))


class VolumeControls(QFrame):
    def __init__(self, parent: QFrame):
        """The controls to allow the user to adjust the media controllers
        output volume. 

        Args:
            parent (QFrame): The parent widget for the media controls.
        """
        super().__init__(parent)
        self.parent = parent
        self.volume = 1
        self.muted = False

        # Connect the controls to their stylesheet. 
        self.setObjectName("VolumeControls")

        # Setup the layout.
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        # Create the mute button and connect it to its call function. 
        self.mute_btn = QPushButton(objectName="mute_btn", flat=True,
                                    icon=QIcon(r"ui\assets\mute_off_2.svg"))
        self.mute_btn.clicked.connect(self.mute_btn_pressed)

        # Create the volume bar and connect it to its value changed function.
        self.volume_bar = QSlider(Qt.Orientation.Horizontal,
                                  objectName="volume_bar")
        self.volume_bar.setRange(0, 100)
        self.volume_bar.setValue(100)
        self.volume_bar.valueChanged.connect(self.volume_changed)
        self.volume_bar.setSizePolicy(QSizePolicy.Policy.Maximum,
                                      QSizePolicy.Policy.Maximum)

        # Add the widgets to the layout. 
        self.layout.addStretch(1)
        self.layout.addWidget(
            self.mute_btn, alignment=Qt.AlignmentFlag.AlignRight)
        self.layout.addWidget(
            self.volume_bar, alignment=Qt.AlignmentFlag.AlignLeft)

    def mute_btn_pressed(self):
        """Toggles the mute state of the media controller and updates the
        widgets to match. 
        """
        if self.muted:
            self.muted = False
            self.volume_changed()
            self.volume_bar.setEnabled(True)
        else:
            self.muted = True
            self.mute_btn.setIcon(QIcon(r"ui\assets\mute_on.svg"))
            self.volume_bar.setEnabled(False)
            self.parent.controls.set_volume(0)

    def volume_changed(self):
        """Updates the volume of the media controller based on the current
        volume slider positon. 
        """
        # Get the value.
        self.volume = self.volume_bar.value()

        # Update the mute button icon.
        if self.volume > 66:
            self.mute_btn.setIcon(QIcon(r"ui\assets\mute_off_2.svg"))
        elif self.volume > 33:
            self.mute_btn.setIcon(QIcon(r"ui\assets\mute_off_1.svg"))
        else:
            self.mute_btn.setIcon(QIcon(r"ui\assets\mute_off_0.svg"))

        # Set the media controller volume. 
        self.parent.controls.set_volume(self.volume/100)

    def resizeEvent(self, a0: QResizeEvent | None) -> None:
        """The function called when the volume controls are resized. Used to 
        enforce sizing for icons and widgets. 

        Args:
            a0 (QResizeEvent | None): Dummy param required by Qt. 
        """
        
        self.mute_btn.setFixedWidth(self.mute_btn.height())
        self.mute_btn.setFixedHeight(self.mute_btn.height())
        self.volume_bar.setFixedHeight(int(self.mute_btn.height()/2))
        self.mute_btn.setIconSize(QSize(self.mute_btn.width(),
                                        self.mute_btn.width()))
