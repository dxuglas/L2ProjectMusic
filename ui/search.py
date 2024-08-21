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
        super().__init__(parent)

        self.setObjectName("SearchPage")
        self.setStyleSheet(open(r"ui\stylesheets\search.qss").read())

        self.sized = False

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.search_bar = QLineEdit(placeholderText="Search...")
        self.search_bar.textChanged.connect(self.search)

        self.layout.addWidget(
            self.search_bar, alignment=Qt.AlignmentFlag.AlignTop)

        self.scroll_area = QScrollArea()
        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        self.scroll_layout = QVBoxLayout()
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)

        self.frame = QFrame()
        self.frame.setLayout(self.scroll_layout)

        self.scroll_area.setWidget(self.frame)
        self.scroll_area.setWidgetResizable(True)

        self.songs = Songs().load()
        self.song_panels = []

        for song in self.songs:
            panel = SongPanel(self, song)
            self.song_panels.append(panel)
            self.scroll_layout.addWidget(panel)

        self.scroll_layout.addStretch(1)

        self.layout.addWidget(self.scroll_area)

    def search(self):
        keywords = self.search_bar.text().split(" ")

        for panel in self.song_panels:
            song = panel.song
            for keyword in keywords:
                keyword = keyword.strip().casefold()
                name = song.name.casefold()
                artist = song.artist.casefold()
                if keyword not in name and keyword not in artist:
                    panel.hide()
                    break
                else:
                    panel.show()

    def resizeEvent(self, a0: QResizeEvent | None) -> None:
        if self.sized == False:
            font = self.search_bar.font()
            font.setPointSize(int(self.height()/20))
            self.search_bar.setFont(font)
            self.sized = True


class SongArt(QPushButton):
    def __init__(self, parent, song) -> None:
        super().__init__(parent)
        self.parent = parent
        self.song = song

        self.setObjectName("SongArt")

        self.setSizePolicy(QSizePolicy.Policy.Maximum,
                           QSizePolicy.Policy.Expanding)

        self.clicked.connect(self.play)

    def play(self):
        self.window().controls.load(self.song)
        self.window().controls.playlist = None

    def resizeEvent(self, a0: QResizeEvent | None) -> None:
        self.setFixedWidth(self.height())
        self.setIconSize(QSize(self.width(), self.height()))


class SongPanel(QFrame):
    def __init__(self, parent, song) -> None:
        super().__init__(parent)
        self.song = song
        self.parent = parent
        self.sized = False

        self.setObjectName("SongPanel")

        self.setSizePolicy(QSizePolicy.Policy.Preferred,
                           QSizePolicy.Policy.Expanding)

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.art = SongArt(self, song)
        self.name = QLabel(objectName="name")
        self.artist = QLabel(objectName="artist")

        self.add_song_btn = QPushButton(objectName="add_song_btn", flat=True,
                                        icon=QIcon(r"ui\assets\plus_black.svg"))
        self.add_song_btn.clicked.connect(self.song_menu)

        self.load()

        self.layout.addWidget(self.art)
        self.layout.addWidget(self.name, alignment=Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(
            self.artist, alignment=Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(self.add_song_btn)

    def load(self) -> None:
        self.name.setText(self.song.name)
        self.artist.setText(self.song.artist)
        self.art.setIcon(self.song.icon)

    def song_menu(self) -> None:
        self.menu = QMenu(self, objectName="menu")

        self.playlists = Playlists().load()
        for playlist in self.playlists:
            option = self.menu.addAction(playlist["name"])
            option.triggered.connect(
                lambda sacrifice="", name=playlist: self.add_song(name))

        self.menu.exec(QCursor.pos())

    def add_song(self, playlist) -> None:
        playlist["songs"].append(self.song.key)
        CreatePlaylistFile(playlist)
        self.window().library.playlists_scroller.load_playlists()

    def resizeEvent(self, a0: QResizeEvent | None) -> None:
        if self.sized == False:
            self.setFixedHeight(int(self.parent.height()/8))
            self.sized = True

        self.add_song_btn.setFixedWidth(self.add_song_btn.height())

        self.setFixedHeight(self.height())
        font = self.name.font()
        font.setPointSize(int(self.height()/5))
        self.name.setFont(font)
        self.artist.setFont(font)
