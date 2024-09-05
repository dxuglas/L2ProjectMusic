"""This module contains the search page which allows the user to browse their
music library, and all associated widgets. 

Noah Douglas - 6/9/24
"""

from PyQt6.QtWidgets import (
    QFrame,
    QLineEdit,
    QVBoxLayout,
    QPushButton,
    QSizePolicy,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QMenu,
)
from PyQt6.QtGui import (
    QIcon,
    QResizeEvent,
    QCursor
)
from PyQt6.QtCore import (
    Qt,
    QSize
)
from file_handler.load import Songs, Playlists
from file_handler.save import CreatePlaylistFile


class SearchPage(QFrame):
    def __init__(self, parent) -> None:
        """Creates a search page and sets up all of the child elements needed.

        Args:
            parent (QFrame): The parent of the search page.
        """
        super().__init__(parent)

        # Link the page to its stylesheet.
        self.setObjectName("SearchPage")
        self.setStyleSheet(open(r"ui\stylesheets\search.qss").read())

        self.sized = False

        # Set up the layout for the page. 
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Create the search bar and connect it to is update function. 
        self.search_bar = QLineEdit(placeholderText="Search...")
        self.search_bar.textChanged.connect(self.search)

        # Add the search bar to the layout and align it to the top of the page.
        self.layout.addWidget(
            self.search_bar, alignment=Qt.AlignmentFlag.AlignTop)

        # Create the scroll area for search results. 
        self.scroll_area = QScrollArea()
        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        # Create the scroll area layout. 
        self.scroll_layout = QVBoxLayout()
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)

        # Create the frame to contain all search results.
        self.frame = QFrame()
        self.frame.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.frame)
        self.scroll_area.setWidgetResizable(True)

        # Get a list of songs from the users library. 
        self.songs = Songs().load()
        self.song_panels = []

        # Generate a song panel for each song.
        for song in self.songs:
            panel = SongPanel(self, song)
            self.song_panels.append(panel)
            self.scroll_layout.addWidget(panel)

        # Force the song panels to align at the top of the scroll area. 
        self.scroll_layout.addStretch(1)

        self.layout.addWidget(self.scroll_area)

    def search(self):
        """Takes the text from the search bar and removes any songs which 
        do not match either the artist or song name from the contents. 
        """
        # Split the search into each keyword. 
        keywords = self.search_bar.text().split(" ")

        # For every song panel loaded. 
        for panel in self.song_panels:
            song = panel.song 
            name = song.name.casefold()
            artist = song.artist.casefold()
             # For every key word in the users search.
            for keyword in keywords:
                keyword = keyword.strip().casefold()
                # If the keyword is not in the name of the song or the artist.
                if keyword not in name and keyword not in artist:
                    # Hide the panel and break the loop. 
                    panel.hide()
                    break
                else:
                    # Show the panel. 
                    panel.show()

    def resizeEvent(self, a0: QResizeEvent | None) -> None:
        """The function called when the search page is resized. 

        Args:
            a0 (QResizeEvent | None): Dummy param required by Qt.
        """ 
        
        # Scale the search bar size to the page size only on the first resize. 
        if self.sized == False:
            font = self.search_bar.font()
            font.setPointSize(int(self.height()/20))
            self.search_bar.setFont(font)
            self.sized = True


class SongArt(QPushButton):
    def __init__(self, parent: QFrame, song) -> None:
        """Create the song art, which also acts as the play button.

        Args:
            parent (QFrame): The parent song panel of the art. 
            song (LoadSong): The loaded song object.
        """
        super().__init__(parent)
        self.parent = parent
        self.song = song

        # Link the button to its stylesheet. 
        self.setObjectName("SongArt")

        self.setSizePolicy(QSizePolicy.Policy.Maximum,
                           QSizePolicy.Policy.Expanding)

        # Connect the button to its call function.
        self.clicked.connect(self.play)

    def play(self):
        """Play the song the art belongs too.
        """
        # Request the controls load the song.
        self.window().controls.load(self.song)
        # Set the current playlist to None, to disable to forward track button.
        self.window().controls.playlist = None

    def resizeEvent(self, a0: QResizeEvent | None) -> None:
        """The function called when the Song Art is resized. 

        Args:
            a0 (QResizeEvent | None): Dummy param required by Qt.
        """
        # Inforce the art sizes to prevent scaling. 
        self.setFixedWidth(self.height())
        self.setIconSize(QSize(self.width(), self.height()))


class SongPanel(QFrame):
    def __init__(self, parent, song) -> None:
        """Creates the song panel which displays the data of a song for the
        search results

        Args:
            parent (QFrame): The parent widget of the panel. 
            song (LoadSong): The loaded song data for the panel. 
        """
        super().__init__(parent)
        self.song = song
        self.parent = parent
        self.sized = False

        # Link the panel to its stylesheet. 
        self.setObjectName("SongPanel")

        # Allow unlimited horizontal stretching. 
        self.setSizePolicy(QSizePolicy.Policy.Preferred,
                           QSizePolicy.Policy.Expanding)

        # Setup the layout for the panel. 
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.art = SongArt(self, song)
        self.name = QLabel(objectName="name")
        self.artist = QLabel(objectName="artist")

        # Create the button to add the song to a playlist. 
        self.add_song_btn = QPushButton(objectName="add_song_btn", flat=True,
                                        icon=QIcon(r"ui\assets\plus_black.svg"))
        # Connect it to its call function.
        self.add_song_btn.clicked.connect(self.song_menu)

        # Load the songs data to the name, artist, and art. 
        self.load()

        # Add all of the widgets to the layout. 
        self.layout.addWidget(self.art)
        self.layout.addWidget(self.name, alignment=Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(
            self.artist, alignment=Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(self.add_song_btn)

    def load(self) -> None:
        """Set the name, artist, and art of the panel to match that of the song.
        """
        self.name.setText(self.song.name)
        self.artist.setText(self.song.artist)
        self.art.setIcon(self.song.icon)

    def song_menu(self) -> None:
        """Opens a menu that allows users to add their song to any playlist
        in their library. 
        """

        # Create the menu. 
        self.menu = QMenu(self, objectName="menu")

        # Load all playlists and add them as options. 
        self.playlists = Playlists().load()
        for playlist in self.playlists:
            option = self.menu.addAction(playlist["name"])
            # Connect each button to its call function.
            option.triggered.connect(
                lambda sacrifice="", name=playlist: self.add_song(name))

        # Open the menu at the cursor position. 
        self.menu.exec(QCursor.pos())

    def add_song(self, playlist: dict) -> None:
        """Resave the playlist file, adding the new song to its list of songs. 

        Args:
            playlist (dict): The playlist data. 
        """
        
        # Update the playlist data to include the new song. 
        playlist["songs"].append(self.song.key)
        # Save the updated file.
        CreatePlaylistFile(playlist)
        # Reload the libraries playlist selector. 
        self.window().library.playlists_scroller.load_playlists()

    def resizeEvent(self, a0: QResizeEvent | None) -> None:
        """The function called when a song panel is resized. 

        Args:
            a0 (QResizeEvent | None): Dummy param required by Qt. 
        """

        # Scale the song panels height to the page only on first resize. 
        if self.sized == False:
            self.setFixedHeight(int(self.parent.height()/8))
            self.sized = True

        # Inforce sizing for widgets
        self.add_song_btn.setFixedWidth(self.add_song_btn.height())
        self.setFixedHeight(self.height())

        # Scale the font size to be 1/5 the height of the panel. 
        font = self.name.font()
        font.setPointSize(int(self.height()/5))
        self.name.setFont(font)
        self.artist.setFont(font)
