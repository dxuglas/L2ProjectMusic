"""This module contains the page handler which acts a parent for the currently
displayed page and handles reinstancing of pages when they are swapped. 

Noah Douglas - 6/9/24
"""

from PyQt6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QSizePolicy
)
from qframelesswindow import (
    TitleBar as QTitleBar
)
from .playlist import PlaylistPage
from .home import HomePage
from .search import SearchPage


class PageHandler(QFrame):
    """The page handler contains and switches between the different pages of 
    the interface. 
    """

    def __init__(self, parent) -> None:
        """Initialises the page handler.

        Args:
            parent (MainWindow): The parent window of the page handler
        """
        super().__init__(parent)
        self.page = None

        # Force the page handler to be its maximum size always.
        self.setSizePolicy(QSizePolicy.Policy.Expanding,
                           QSizePolicy.Policy.Expanding)

        # Create a title bar, which is refrenced in the main window as the
        # windows title bar.
        self.title_bar = QTitleBar(self)

        # Setup the layout for the widget, offsetting vertically for the
        # title bar.
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(
            0, self.title_bar.frameGeometry().height(), 0, 0)
        self.setLayout(self.layout)

        self.update_page("home")

    def update_page(self, type: str, data=None) -> None:
        """Updates the page handlers page to be the type passed.

        Args:
            type (str): The type of page. 
            data (dict, optional): Data for the page that is being loaded. 
            Defaults to None.
        """

        # First delete the current page.
        if self.page:
            self.page.deleteLater()
            self.page = None

        # Check the type of page requested and load it.
        if type == "playlist":
            self.page = PlaylistPage(self, data)
        elif type == "home":
            self.page = HomePage(self)
        elif type == "search":
            self.page = SearchPage(self)

        # Add the page to the layout and update the status of the handler.
        self.layout.addWidget(self.page)
        self.status = type
