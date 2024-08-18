from qframelesswindow import (
    FramelessWindow as QWindow,
)
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout
)
from PyQt6.QtCore import (
    Qt,
    QTimer
)
from .media_interface import MediaInterface
from .library import Library
from .page import PageHandler
from media_handler.controls import Controls


class MainWindow(QWindow):
    def __init__(self, parent) -> None:
        super().__init__()

        self.parent = parent

        self.controls = Controls(self)

        self.setStyleSheet(open(r"ui\stylesheets\ui.qss").read())

        self.screen_size = self.get_screen_size()
        self.setMinimumSize(int(self.screen_size[0]/2),
                            int(self.screen_size[0]/2.82))

        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.center_layout = QHBoxLayout()
        self.center_layout.setSpacing(0)
        self.center_layout.setContentsMargins(0, 0, 0, 0)

        self.library = Library(self)
        self.center_layout.addWidget(self.library,
                                     alignment=Qt.AlignmentFlag.AlignLeft)

        self.page_handler = PageHandler(self)
        self.center_layout.addWidget(self.page_handler)

        self.media_layout = QHBoxLayout()
        self.media_layout.setContentsMargins(0, 0, 0, 0)

        self.media_interface = MediaInterface(self)

        self.media_layout.addWidget(self.media_interface,
                                    alignment=Qt.AlignmentFlag.AlignBottom)

        self.layout.addLayout(self.center_layout)
        self.layout.addLayout(self.media_layout)

        self.setTitleBar(self.page_handler.title_bar)

        self.timer = QTimer(self, singleShot=False, interval=500)
        self.timer.timeout.connect(self.update_media)
        self.timer.start()

    def get_screen_size(self):
        screen_size = self.parent.primaryScreen().size()

        return [screen_size.width(), screen_size.height()]

    def get_window_size(self):
        return [self.width(), self.height()]

    def update_page(self, type, data=None):
        self.page_handler.update_page(type, data)

    def update_media(self):
        self.controls.update()
