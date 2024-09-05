"""This module contains the file dialog which allows the users to browse their
file system from in my program.

Noah Douglas - 6/9/24
"""

from PyQt6.QtWidgets import QFileDialog
import os


class Selector(QFileDialog):
    """A file selector window pop up for user uploaded data."""

    def __init__(self) -> None:
        """Intialises a file dialog to allow users to browse their computer
        for files to upload.
        """
        super().__init__()

        self.setModal(True)  # Always on top
        self.setOption(QFileDialog.Option.ReadOnly, True)

        self.image_exts = "*.jpg *.jpeg *.png *.webp *.svg"
        self.song_exts = "*.mp3 *.wav *.ogg"

    def get_file(self, type: str) -> list:
        """Open the file dialog using provided type for filters.

        Args:
            type (str): The type of file needed.

        Returns:
            list: The file selected.
        """
        if type == "image":
            ext = self.image_exts
            dir = f'~/Pictures'
        elif type == "song":
            ext = self.song_exts
            dir = f'~/Music'
        return self.getOpenFileName(filter=ext,
                                    directory=os.path.expanduser(dir))
