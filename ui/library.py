from PyQt6.QtWidgets import (
    QFrame,
    QPushButton,
    QVBoxLayout,
    QScrollArea,
    QMenu
)
from PyQt6.QtCore import (
    QSize,
    Qt
)
from PyQt6.QtGui import (
    QIcon,
    QResizeEvent,
    QCursor
)
from .popups.creation import CreatePlaylist, UploadSong
from file_handler.load import Playlists


class Library(QFrame):
    def __init__(self, parent) -> None:
        """Initialises the library panel, which includes menu buttons, and the
        buttons to open different playlists. 

        Args:
            parent (MainWindow): The parent widget of the Library. 
        """
        super().__init__(parent)
        self.parent = parent

        # Link the widget to its stylesheet. 
        self.setObjectName("Library")
        self.setStyleSheet(open(r"ui\stylesheets\library.qss").read())

        # Get and set the width of the library
        self.width = int(self.parent.screen_size[0]*0.05)
        self.setFixedWidth(self.width)

        # Create the layout for library contents.
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.menu_buttons = MenuButtons(self)
        self.layout.addWidget(self.menu_buttons)

        self.playlists_scroller = PlaylistScroller(self)
        self.layout.addWidget(self.playlists_scroller)


class MenuButtons(QFrame):
    def __init__(self, parent: QFrame) -> None:
        """Intialises the Menu Buttons, which allow the user to go to the home
        page, search page, and access upload/creation menus. 

        Args:
            parent (QFrame): The parent widget of the MenuButtons. 
        """
        super().__init__(parent)
        self.parent = parent

        # Link the widget to its stylesheet.
        self.setObjectName("MenuButtons")

        # Setup the layout for Menu contents. 
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(10, 5, 10, 5)
        self.layout.setSpacing(10)
        self.setLayout(self.layout)

        # Create the menu buttons, and link them to their call functions.
        self.home_btn = QPushButton(objectName="home_btn", flat=True,
                                    icon=QIcon(r"ui\assets\home.svg"))
        self.home_btn.clicked.connect(self.home)

        self.search_btn = QPushButton(objectName="search_btn", flat=True,
                                      icon=QIcon(r"ui\assets\search.svg"))
        self.search_btn.clicked.connect(self.search)

        self.new_btn = QPushButton(objectName="new_btn", flat=True,
                                   icon=QIcon(r"ui\assets\plus_white.svg"))
        self.new_btn.clicked.connect(self.new)

        # Add the buttons to the layout.
        self.layout.addWidget(self.home_btn)
        self.layout.addWidget(self.search_btn)
        self.layout.addWidget(self.new_btn)

    def home(self) -> None:
        """Requests the page handler load the Home page.
        """
        self.window().update_page("home")

    def search(self) -> None:
        """Requests the page handler load the Search page. 
        """

        self.window().update_page("search")

    def new(self) -> None:
        """Generates a menu to allow the user to choose whether they upload a 
        song or create a playlist. 
        """

        # Create the Menu.
        self.menu = QMenu(self, objectName="menu")

        # Add the actions and link them to their call functions. 
        upload_song = self.menu.addAction("Upload Song")
        create_playlist = self.menu.addAction("Create Playlist")

        upload_song.triggered.connect(self.upload_song)
        create_playlist.triggered.connect(self.create_playlist)

        # Load the menu at the cursor position.
        self.menu.exec(QCursor.pos())

    def upload_song(self) -> None:
        """Open a Song Upload pop up. 
        """
        self.popup = UploadSong(self.window())
        self.popup.exec()

    def create_playlist(self) -> None:
        """Opens a Playlist Creation pop up.
        """
        self.popup = CreatePlaylist(self.window())
        self.popup.exec()

        # Reload the playlists in the playlist scroller. 
        self.parent.playlists_scroller.load_playlists()

    def resizeEvent(self, a0: QResizeEvent | None) -> None:
        """Called when the Menu Buttons are resized, used to enforce icon size
        scaling. 

        Args:
            a0 (QResizeEvent | None): Dummy param required by Qt.
        """

        self.home_btn.setIconSize(QSize(self.home_btn.width(),
                                        self.home_btn.width()))
        self.search_btn.setIconSize(QSize(self.search_btn.width(),
                                          self.search_btn.width()))
        self.new_btn.setIconSize(QSize(self.new_btn.width(),
                                       self.new_btn.width()))


class PlaylistButton(QPushButton):
    def __init__(self, parent: QFrame, playlist: dict) -> None:
        """Creates a playlist button to be added to the playlist scroller, and
        when clicked loads the playlist page. 

        Args:
            parent (QFrame): The parent of the button.
            playlist (dict): Data of the playlist the button is for. 
        """
        super().__init__(parent)
        self.parent = parent
        self.playlist = playlist

        # Link to stylesheet. 
        self.setObjectName("PlaylistButton")

        # Configure the icon
        self.setIcon(QIcon(playlist["icon"]))
        self.setFlat(True)

        # Connect the button to its call function
        self.clicked.connect(self.load_playlist)

    def load_playlist(self) -> None:
        """Request the page handler to load the playlist page, using the data
        passed. 
        """
        self.window().update_page("playlist", self.playlist)

    def resizeEvent(self, a0: QResizeEvent | None) -> None:
        """The function called when the button is resized. 

        Args:
            a0 (QResizeEvent | None): Dummy param required by Qt.
        """
        self.setFixedSize(QSize(self.parent.width(), self.parent.width()))
        self.setIconSize(QSize(self.width(), self.height()))


class PlaylistScroller(QScrollArea):
    def __init__(self, parent: QFrame) -> None:
        """Creates the playlist scroll area, which contains all of the playlist
        buttons. 

        Args:
            parent (QFrame): The parent of the scroll area. 
        """
        super().__init__(parent)

        self.playlists = None

        # Disable the horizontal scroll bar and force the vertical to show. 
        self.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        # Create the layout and the frame to hold all of the buttons. 
        self.layout = QVBoxLayout()
        self.frame = QFrame(self, objectName="playlists")
        self.setWidget(self.frame)
        self.setWidgetResizable(True)

        # Load the playlist buttons. 
        self.load_playlists()

    def load_playlists(self) -> None:
        """Resets the playlist scroll area and then loads all playlist files.
        """
        # Set the layout to a temporary widget to delete it.
        QFrame().setLayout(self.layout)

        # Create a new layout.
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.frame.setLayout(self.layout)

        # Load all of the users playlists. 
        self.playlists = Playlists().load()

        # Generate a playlist button for every playlist.
        for playlist in self.playlists:
            self.layout.addWidget(PlaylistButton(self, playlist),
                                  alignment=Qt.AlignmentFlag.AlignCenter)

        # Force the playlists to arrange at the top of the scroll area. 
        self.layout.addStretch(1)


        
