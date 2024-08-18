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
    def __init__(self, parent) -> None:
        super().__init__(parent)

        self.setObjectName("HomePage")
        self.setStyleSheet(open(r"ui\stylesheets\home.qss").read())

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(self.layout)

        self.recommendation_panel = RecommendationPanel(self)
        self.similar_song_panel = SimilarSongsPanel(self)

        self.layout.addWidget(self.recommendation_panel, stretch=1)
        self.layout.addWidget(self.similar_song_panel, stretch=1)


class DisplayPanel(QFrame):
    def __init__(self, parent, placeholder_text) -> None:
        super().__init__(parent)

        self.placeholder_text = placeholder_text

        self.setObjectName("DisplayPanel")

        self.layout = QGridLayout()
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(self.layout)

        self.title = QLabel(objectName="title")

        self.title_layout = QHBoxLayout()
        self.title_layout.setContentsMargins(0, 0, 0, 0)

        self.refresh_button = QPushButton(objectName="refresh",
                                          flat=True,
                                          icon=QIcon(r"ui\assets\refresh.svg"))
        self.refresh_button.clicked.connect(self.refresh)

        self.title_layout.addWidget(self.title)
        self.title_layout.addWidget(self.refresh_button)

        self.layout.addLayout(self.title_layout, 0, 0, 1, 2)
        self.layout.setSpacing(10)

        self.refresh()

    def refresh(self) -> None:
        index = self.layout.count()
        while (index >= 0):
            item = self.layout.itemAt(index)
            if item:
                widget = item.widget()
                if widget:
                    widget.setParent(None)
            index -= 1

        for x in range(2):
            for y in range(2):
                panel = SongPanel(
                    self, self.placeholder_text, self.songs[2*x+y])
                self.layout.addWidget(panel, x+1, y)

    def resizeEvent(self, a0: QResizeEvent | None) -> None:

        self.refresh_button.setFixedWidth(self.refresh_button.height())

        font = self.title.font()
        font.setPointSize(int(self.height()/8))
        self.title.setFont(font)


class RecommendationPanel(DisplayPanel):
    def __init__(self, parent) -> None:
        super().__init__(parent, "Try Uploading More Songs!")
        self.title.setText("Songs from your library")

    def refresh(self) -> None:
        self.songs = SongRecommendations().from_library(4)

        super().refresh()


class SimilarSongsPanel(DisplayPanel):
    def __init__(self, parent) -> None:
        self.song = LoadSong(SongRecommendations().from_library(1)[0])
        super().__init__(parent, "Cannot load songs, try again later")

    def refresh(self) -> None:
        previous_song = self.song
        while self.song.name == previous_song.name:
            self.song = LoadSong(SongRecommendations().from_library(1)[0])

        self.title.setText(f"Because you liked... {self.song.name}")

        self.songs = SongRecommendations().from_shazam(self.song.key, 4)

        super().refresh()


class SongArt(QPushButton):
    def __init__(self, parent, song) -> None:
        super().__init__(parent)
        self.parent = parent
        self.song = song

        if isinstance(self.song, str):
            self.clicked.connect(self.play)
        else:
            self.clicked.connect(self.open)

        self.setObjectName("SongArt")

        self.setSizePolicy(QSizePolicy.Policy.Maximum,
                           QSizePolicy.Policy.Expanding)

    def play(self):
        track = LoadSong(self.song)
        self.window().controls.load(track)
        self.window().controls.playlist = None

    def open(self):
        try:
            webbrowser.open(self.song["hub"]["actions"][1]["uri"])
        except:
            pass

    def resizeEvent(self, a0: QResizeEvent | None) -> None:
        self.setFixedWidth(self.height())
        self.setIconSize(QSize(self.width(), self.height()))


class SongPanel(QFrame):
    def __init__(self, parent, placeholder_text, song=None) -> None:
        super().__init__(parent)
        self.song = song
        self.parent = parent
        self.placeholder_text = placeholder_text

        self.setObjectName("SongPanel")

        self.setSizePolicy(QSizePolicy.Policy.Preferred,
                           QSizePolicy.Policy.Expanding)

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
        if isinstance(self.song, str):
            data = LoadSong(self.song)
        elif isinstance(self.song, dict):
            data = LoadSong(None, self.song)

        self.name.setText(data.name)
        self.art.setIcon(data.icon)

    def resizeEvent(self, a0: QResizeEvent | None) -> None:
        font = self.name.font()
        font.setPointSize(int(self.height()/4))
        self.name.setFont(font)
