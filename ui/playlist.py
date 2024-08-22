from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QScrollArea,
    QSizePolicy
)
from PyQt6.QtCore import (
    QSize,
    Qt
)
from PyQt6.QtGui import (
    QIcon,
    QResizeEvent
)
from file_handler.load import LoadSong


class PlaylistPage(QFrame):
    def __init__(self, parent: QFrame, playlist: dict = None) -> None:
        """The is the initialise function for the Playlist Page. It setup up
        all the neccesary widgets and loads the playlists data. 

        Args:
            parent (QFrame): The parent widget which will contain the page. 
            playlist (dict, optional): Playlist data. Defaults to None.
        """
        super().__init__(parent)
        self.playlist = playlist

        # Link the page to its stylesheet.
        self.setObjectName("PlaylistPage")
        self.setStyleSheet(open(r"ui\stylesheets\playlist.qss").read())

        # Setup the layout, with a 10px margin around the outside.
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(self.layout)

        # Create the panels to display on the page and add them to the layout.
        self.header = HeaderPanel(self, self.playlist)
        self.song_viewer = SongViewer(self, self.playlist)

        self.layout.addWidget(self.header, stretch=5)
        self.layout.addWidget(self.song_viewer, stretch=6)


class HeaderPanel(QFrame):
    def __init__(self, parent: QFrame, playlist: dict) -> None:
        """The header panel which contains all of the playlists information. 

        Args:
            parent (QFrame): The parent widget of the panel. 
            playlist (dict): The playlist data. 
        """
        super().__init__(parent)
        self.playlist = playlist

        # Link the panel to its stylesheet.
        self.setObjectName("HeaderPanel")

        # Set up the layout.
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        # The playlist art display.
        self.art = PlaylistArt(self, playlist)
        self.art.setSizePolicy(QSizePolicy.Policy.Expanding,
                               QSizePolicy.Policy.Expanding)
        self.layout.addWidget(self.art, stretch=1)

        # Create the playout to contain the text content.
        self.text_layout = QVBoxLayout()
        self.text_layout.setContentsMargins(0, 0, 0, 0)

        # The playlist name a description fields.
        self.name = QPushButton(objectName="name", flat=True)
        self.desc = QLabel(objectName="desc")

        # Add the labels to the text layout.
        self.text_layout.addStretch(1)
        self.text_layout.addWidget(
            self.name, alignment=Qt.AlignmentFlag.AlignLeft, stretch=1)
        self.text_layout.addWidget(
            self.desc,
            alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop,
            stretch=1)

        # Create a container to parent the text layout, so you can add stretch.
        self.text_container = QFrame()
        self.text_container.setLayout(self.text_layout)

        # Add the container to the main layout. 
        self.layout.addWidget(self.text_container, stretch=2)

        # If there is a playlist load it, otherwise set the placeholders. 
        if playlist:
            self.load()
        else:
            self.art.setIcon(QIcon(r"ui\assets\placeholder.svg"))
            self.name.setText("Playlist")
            self.desc.setText("")

    def load(self):
        """Load the playlists data to the child widgets. 
        """
        self.art.setIcon(QIcon(self.playlist["icon"]))
        self.name.setText(self.playlist["name"])
        self.desc.setText(self.playlist["description"])

    def resizeEvent(self, a0: QResizeEvent | None) -> None:
        """The function called when the panel is resized, used to scaled text
        sizes. 

        Args:
            a0 (QResizeEvent | None): Dummy param required by Qt.
        """

        # Set the font size of the name to 1/7 the height of the panel. 
        font = self.name.font()
        font.setPointSize(int(self.height()/7))
        self.name.setFont(font)


class PlaylistArt(QPushButton):
    def __init__(self, parent: QFrame, playlist: dict):
        super().__init__(parent)
        self.playlist = playlist

        # Link the button to its stylesheet. 
        self.setObjectName("playlist_art")
        self.setFlat(True)

        self.setSizePolicy(QSizePolicy.Policy.Maximum,
                           QSizePolicy.Policy.Maximum)

    def resizeEvent(self, a0: QResizeEvent | None) -> None:
        """The function called when the button is resized. Used to enforce 
        sizing.

        Args:
            a0 (QResizeEvent | None): Dummy param required by Qt. 
        """
        # Force the art to be square. 
        self.setFixedWidth(self.height())

        # Change the icon scaling depending on if the placeholder icon is used. 
        if self.playlist:
            self.setIconSize(QSize(self.width(), self.height()))
        else:
            self.setIconSize(QSize(int(self.width()/2), int(self.height()/2)))


class SongPanel(QFrame):
    def __init__(self, parent, song=None, playlist=None):
        """A song panel which displays a songs data.

        Args:
            parent (QFrame): The parent of the panel.
            song (LoadSong, optional): The panels song. Defaults to None.
            playlist (dict, optional): The playlist the song belongs to. 
            Defaults to None.
        """
        super().__init__(parent)
        self.song = song
        self.playlist = playlist
        self.parent = parent
        self.sized = False

        # Link the panel to its style sheet. 
        self.setObjectName("SongPanel")

        self.setSizePolicy(QSizePolicy.Policy.Preferred,
                           QSizePolicy.Policy.Maximum)

        # Set up the layout with 0 px margins. 
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        # Create the information display widgets. 
        self.art = SongArt(self, song, playlist)
        self.name = QLabel(objectName="name")
        self.artist = QLabel(objectName="artist")

        # If the panel has a song, attempt to load it, otherwise use defaults. 
        if song:
            self.load()
        else:
            self.art.setIcon(QIcon(r"ui\assets\placeholder.svg"))
            self.name.setText("Song")
            self.artist.setText("Artist")

        # Add all of the information widgets to the layout. 
        self.layout.addWidget(self.art)
        self.layout.addWidget(
            self.name, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(
            self.artist, alignment=Qt.AlignmentFlag.AlignCenter)

    def load(self):
        """Load the songs data, and then configure the information display
        widgets to match it. 
        """
        song_data = LoadSong(self.song)
        self.art.setIcon(song_data.icon)
        self.name.setText(song_data.name)
        self.artist.setText(song_data.artist)

    def resizeEvent(self, a0: QResizeEvent | None) -> None:
        """The function called when the song panel is resized. Used to enforce
        size restrictions on the widget. 

        Args:
            a0 (QResizeEvent | None): Dummy param required by Qt. 
        """

        # Scale the panel on the first resize only. 
        if not self.sized:
            self.sized = True
            self.setMinimumHeight(int(self.parent.height()/5))

        self.setFixedHeight(self.height())


class SongArt(QPushButton):
    def __init__(self, parent, song: str, playlist: dict):
        """A songs art display panel, and also the play button to listen to the
        song. 

        Args:
            parent (_type_): The parent panel of the art.
            song (str): The song to be displayed/played
            playlist (dict): The playlist the panel is in. 
        """
        super().__init__(parent)
        self.parent = parent
        self.song = song
        self.playlist = playlist

        # Link the art to its style sheet. 
        self.setObjectName("song_art")
        self.setFlat(True)

        # Connect the button to its call function. 
        self.clicked.connect(self.play)

    def play(self):
        """Loads the song data, and passes it to the media controller for it to
        be played. 
        """
        track = LoadSong(self.song)
        self.window().controls.load(track)
        self.window().controls.playlist = self.playlist

    def resizeEvent(self, a0: QResizeEvent | None) -> None:
        """The function called when the art is resized. Used to enforce size
        restrictions and also to scale the icon correctly.

        Args:
            a0 (QResizeEvent | None): Dummy param required by Qt. 
        """

        self.setFixedSize(QSize(self.parent.height(), self.parent.height()))

        # Set the icon size depending on if the placeholder is in use. 
        if self.song:
            self.setIconSize(QSize(self.width(), self.height()))
        else:
            self.setIconSize(QSize(int(self.width()/2), int(self.height()/2)))


class SongViewer(QScrollArea):
    def __init__(self, parent, playlist: dict):
        """Intialises the song viewer, which allows the user to scroll through
        the songs in a library. 

        Args:
            parent (QFrame): The parent widget of the song viewer.
            playlist (dict): The playlist the viewer is for. 
        """
        super().__init__(parent)
        self.playlist = playlist

        # Disable the horizontal scroll bar and force the vertical bar to show. 
        self.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        # Create the layout for the viewer, and also the frame to contain the
        # song panels. 
        self.layout = QVBoxLayout()
        self.frame = QFrame(self, objectName="songs")
        self.frame.setLayout(self.layout)

        # For every song in the playlist generate a song panel, and add it
        # to the layout. 
        for song in self.playlist["songs"]:
            widget = SongPanel(self, song, self.playlist)
            self.layout.addWidget(widget)

        # Add stretch to force the songs to the top of the frame.
        self.layout.addStretch(1)

        self.setWidget(self.frame)
        self.setWidgetResizable(True)

    def resizeEvent(self, a0: QResizeEvent | None) -> None:
        """The function called when the song viewer is resized, used to enforce
        sizing restrictions. 

        Args:
            a0 (QResizeEvent | None): Dummy param required by Qt. 
        """
        self.frame.setFixedWidth(self.width())
        self.setMinimumHeight(self.height())
