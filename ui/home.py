"""This module contains the home page of the UI, and any widgets required to
build this page.

Noah Douglas - 6/9/24
"""

from PyQt6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QGridLayout,
    QSizePolicy,
    QHBoxLayout,
    QLabel,
    QPushButton
)
from PyQt6.QtGui import (
    QIcon,
    QResizeEvent
)
from PyQt6.QtCore import (
    Qt,
    QSize
)
from media_handler.song_recommendations import SongRecommendations
from file_handler.load import LoadSong
import webbrowser


class HomePage(QFrame):
    def __init__(self, parent: QFrame) -> None:
        """This is the initialise function for the Home Page class, which
        setups up all of the neccesary child widgets.

        Args:
            parent (QFrame): The parent widget which will contain the page
        """
        super().__init__(parent)

        # Link the page to its style sheet information.
        self.setObjectName("HomePage")
        self.setStyleSheet(open(r"ui\stylesheets\home.qss").read())

        # Setup the layout, with 10 px of margin around the outside.
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(self.layout)

        # Create panels to display on the page and add them to the layout.
        self.recommendation_panel = RecommendationPanel(self)
        self.similar_song_panel = SimilarSongsPanel(self)
        self.layout.addWidget(self.recommendation_panel, stretch=1)
        self.layout.addWidget(self.similar_song_panel, stretch=1)


class DisplayPanel(QFrame):
    def __init__(self, parent: QFrame, placeholder_text: str) -> None:
        """This is the instialise function of the Display Panel class, which
        acts as a base class for the different types of display panels on the
        home page. This function loads all the neccesary information and
        sets up the panel.

        Args:
            parent (QFrame): The parent widget which will contain the panel.
            placeholder_text (str): The placeholder text for empty song names.
        """
        super().__init__(parent)
        self.placeholder_text = placeholder_text

        # Link to the stylesheet.
        self.setObjectName("DisplayPanel")

        # Setup the layout, with 10 px of margin around the outside.
        self.layout = QGridLayout()
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(self.layout)

        # Setup the title layout, with 0 px of margin.
        self.title_layout = QHBoxLayout()
        self.title_layout.setContentsMargins(0, 0, 0, 0)

        self.title = QLabel(objectName="title")

        # Create a button to refresh the songs on the panel.
        self.refresh_button = QPushButton(objectName="refresh",
                                          flat=True,
                                          icon=QIcon(r"ui\assets\refresh.svg"))
        self.refresh_button.clicked.connect(self.refresh)

        # Add the title widgets to the title layout.
        self.title_layout.addWidget(self.title)
        self.title_layout.addWidget(self.refresh_button)

        # Place the title layout in the grid, y:0, x:0, y-span:1, x-span:2.
        self.layout.addLayout(self.title_layout, 0, 0, 1, 2)
        self.layout.setSpacing(10)

        self.refresh()  # Load songs to the panel.

    def refresh(self) -> None:
        """This function first clears all child widgets, and then generates
        new song panels and adds them to the display panel.
        """

        index = self.layout.count()
        # For every widget in the panel, remove it.
        while (index >= 0):
            item = self.layout.itemAt(index)
            if item:
                widget = item.widget()
                if widget:
                    widget.setParent(None)
            index -= 1

        # Generate 4 song panels, arranging them in the grid layout in 2 rows.
        for x in range(2):
            for y in range(2):
                panel = SongPanel(
                    self, self.placeholder_text, self.songs[2*x+y])
                self.layout.addWidget(panel, x+1, y)

    def resizeEvent(self, a0: QResizeEvent | None) -> None:
        """The function called when the display panel is resized, which is used
        to enforce sizing and scale text sizes.

        Args:
            a0 (QResizeEvent | None): A dummy parameter required by Qt
        """

        self.refresh_button.setFixedWidth(self.refresh_button.height())

        # Scale the title size to be 1/8 the height of the panel.
        font = self.title.font()
        font.setPointSize(int(self.height()/8))
        self.title.setFont(font)


class RecommendationPanel(DisplayPanel):
    def __init__(self, parent: QFrame) -> None:
        """Intialises an instance of the Display Panel class, altering it to
        display data relating to song recommendations from the user library. 

        Args:
            parent (QFrame): The parent widget the panel will be added to.
        """
        super().__init__(parent, "Try Uploading More Songs!")
        self.title.setText("Songs from your library")

    def refresh(self) -> None:
        """Gets songs from the user library and loads them to the display
        panel.
        """
        self.songs = SongRecommendations().from_library(4)
        super().refresh()


class SimilarSongsPanel(DisplayPanel):
    def __init__(self, parent: QFrame) -> None:
        """Initialises an instance of the Display Panel class, altering it to
        display dating about similar songs the user might like using Shazam
        recommendations.

        Args:
            parent (QFrame): The parent widget the panel will be added to.
        """

        super().__init__(parent, "Cannot load songs, try again later")

    def refresh(self) -> None:
        """Gets the song that recommendations will be based on and then loads
        recommendations from shazam.
        """

        # Loads a song from the library
        song = SongRecommendations().from_library(1)

        # Checks a song could be loaded and then loads recommendations
        if song:
            self.song = LoadSong(song[0])
            self.title.setText(f"Because you liked... {self.song.name}")

            self.songs = SongRecommendations().from_shazam(self.song.key, 4)

            super().refresh()


class SongArt(QPushButton):
    def __init__(self, parent: QFrame, song: str | dict) -> None:
        """Initialises the Song Art for display panels.

        Args:
            parent (QFrame): _description_
            song (str | dict): _description_
        """
        super().__init__(parent)
        self.parent = parent
        self.song = song

        # If the song is a file passed as a str, link it to the play function.
        if isinstance(self.song, str):
            self.clicked.connect(self.play)
        # Otherwise link it to the open function.
        else:
            self.clicked.connect(self.open)

        self.setObjectName("SongArt")

        self.setSizePolicy(QSizePolicy.Policy.Maximum,
                           QSizePolicy.Policy.Expanding)

    def play(self) -> None:
        """Load the song file and then pass the media file to the controls.
        """
        track = LoadSong(self.song)
        self.window().controls.load(track)
        self.window().controls.playlist = None

    def open(self) -> None:
        """Try to open the song link in the users web browser. 
        """
        try:
            webbrowser.open(self.song["hub"]["actions"][1]["uri"])
        except:
            pass

    def resizeEvent(self, a0: QResizeEvent | None) -> None:
        """The function called when the art is resized, used to enforce size
        scaling

        Args:
            a0 (QResizeEvent | None): Dummy paramter required by Qt
        """
        self.setFixedWidth(self.height())
        self.setIconSize(QSize(self.width(), self.height()))


class SongPanel(QFrame):
    def __init__(self, parent: QFrame, placeholder_text: str,
                 song: str | dict = None) -> None:
        """Intialises a song panel, loading all of the songs data.

        Args:
            parent (QFrame): The parent widget this panel will be added to.
            placeholder_text (str): The placeholder text for the song name
            song (str | dict, optional): A song to load. Defaults to None.
        """
        super().__init__(parent)
        self.song = song
        self.parent = parent
        self.placeholder_text = placeholder_text

        self.setObjectName("SongPanel")

        self.setSizePolicy(QSizePolicy.Policy.Preferred,
                           QSizePolicy.Policy.Expanding)

       # Setup the layout, with 10 px of margin around the outside.
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.art = SongArt(self, song)
        self.name = QLabel(objectName="name")

        if song:
            self.load()
        else:
            self.art.setIcon(QIcon(r"ui\assets\placeholder.svg"))
            self.name.setText(self.placeholder_text)

        self.layout.addWidget(self.art)
        self.layout.addWidget(self.name, alignment=Qt.AlignmentFlag.AlignLeft)

    def load(self) -> None:
        """Loads a songs data to the panel.
        """

        # Checks if the song passed is a file or shazam data and loads it. 
        if isinstance(self.song, str):
            data = LoadSong(self.song)
        elif isinstance(self.song, dict):
            data = LoadSong(None, self.song)

        self.name.setText(data.name)
        self.art.setIcon(data.icon)

    def resizeEvent(self, a0: QResizeEvent | None) -> None:
        """The function called when the panel is resized, for enforcing text
        scaling

        Args:
            a0 (QResizeEvent | None): Dummy parameter required by Qt
        """
        # Scale the songs name to be 1/5 of the panels height.
        font = self.name.font()
        font.setPointSize(int(self.height()/5))
        self.name.setFont(font)
