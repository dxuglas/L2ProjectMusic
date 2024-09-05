"""This module contains the main window of the UI; the rest of the UI is built
here. 

Noah Douglas - 6/9/24
"""

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
        """The Main Window of the program, which sets up the whole interface,
        and acts as a way to pass data between widgets.

        Args:
            parent (Application): The application the window belongs too. 
        """
        super().__init__()

        self.parent = parent

        # Create a media controller object. 
        self.controls = Controls(self)

        # Connect to the windows stylesheet. 
        self.setStyleSheet(open(r"ui\stylesheets\ui.qss").read())

        # Set the minimum size of the window based on screen size.
        self.screen_size = self.get_screen_size()
        self.setMinimumSize(int(self.screen_size[0]/2),
                            int(self.screen_size[0]/2.82))

        # Set up the windows layout, with 0 pixels of margin. 
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        # Set up the layout to handle the center content of the window.
        self.center_layout = QHBoxLayout()
        self.center_layout.setSpacing(0)
        self.center_layout.setContentsMargins(0, 0, 0, 0)

        # Create a library, and add it too the center content, aligned left. 
        self.library = Library(self)
        self.center_layout.addWidget(self.library,
                                     alignment=Qt.AlignmentFlag.AlignLeft)

        # Create a page handler, and add it too the center content. 
        self.page_handler = PageHandler(self)
        self.center_layout.addWidget(self.page_handler)

        # Create the media layout, to contain the media interface
        self.media_layout = QHBoxLayout()
        self.media_layout.setContentsMargins(0, 0, 0, 0)

        # Create the media interface and add it to the media layout. 
        self.media_interface = MediaInterface(self)
        self.media_layout.addWidget(self.media_interface,
                                    alignment=Qt.AlignmentFlag.AlignBottom)

        # Add both content layouts to the main layout. 
        self.layout.addLayout(self.center_layout)
        self.layout.addLayout(self.media_layout)

        # Set the windows title bar, which contains window controls.
        self.setTitleBar(self.page_handler.title_bar)

        # Begin a timer which runs the update function every 0.5 seconds. 
        self.timer = QTimer(self, singleShot=False, interval=500)
        self.timer.timeout.connect(self.controls.update)
        self.timer.start()

    def get_screen_size(self) -> list:
        """Gets the primary display size and returns it as a list. 

        Returns:
            list: The screen size.
        """

        screen_size = self.parent.primaryScreen().size()

        return [screen_size.width(), screen_size.height()]

    def get_window_size(self) -> list:
        """Get the size of the window, which is used by child widgets for 
        sizing.

        Returns:
            list: The size of the window.
        """
        return [self.width(), self.height()]

    def update_page(self, type: str, data=None):
        """Requests the page handler update the page.

        Args:
            type (str): The type of page to be loaded
            data (dict, optional): Any data for the page. Defaults to None.
        """
        self.page_handler.update_page(type, data)