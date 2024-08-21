import json
import os
import requests

from PyQt6.QtGui import (
    QIcon,
    QPixmap
)

DIRECTORY = os.path.expanduser(f'~/AppData/Local/Musi')

if not os.path.exists(DIRECTORY):
    os.mkdir(DIRECTORY)
    os.mkdir(fr"{DIRECTORY}/Playlists/")
    os.mkdir(fr"{DIRECTORY}/Songs/")


class Playlists():
    def __init__(self) -> None:
        """This is the init function for the Playlist loader
        """
        self.dir = "Playlists"
        self.playlists = []

    def load(self) -> list:
        """This function iterates through every file in the playlist directory
        and loads them.

        Returns:
            list: A list of loaded playlist files.
        """

        # For every file in the playlist directory
        for file in os.listdir(fr"{DIRECTORY}/{self.dir}"):
            self.playlists.append(LoadFile(self.dir, file).load())

        return self.playlists


class Songs():
    def __init__(self) -> None:
        """This is the intialisation function for the Song loader
        """
        self.dir = "Songs"
        self.songs = []

    def load(self) -> list:
        """This function iterates through every file in the song directory and
        loads them.

        Returns:
            list: A list of loaded song files
        """

        for file in os.listdir(fr"{DIRECTORY}/{self.dir}"):
            self.songs.append(LoadSong(file))

        return self.songs


class LoadFile():
    def __init__(self, dir: str, file: str) -> None:
        """This is the init function for file loader, which checks to ensure
        the file can actually exist.

        Args:
            dir (str): The directory the file is located
            file (str): The file name
        """

        self.dir = fr"{DIRECTORY}/{dir}/"
        self.file = file

        # Check the file has a json extension, as sometimes files will be
        # returned without any extension. 
        if self.file:
            if ".json" not in self.file:
                self.file += ".json"

        # Check the directory exists and if it doesn't create it. 
        if not os.path.exists(self.dir):
            os.mkdir(self.dir)

    def load(self) -> dict | None:
        """Attempts to load the file

        Returns:    
            dict: The song data, if loaded failed defaults to None.
        """
        try:
            with open(fr"{self.dir}/{self.file}", 'r') as f:
                self.file = json.load(f)
        except:
            self.file = None

        return self.file


class LoadSong(LoadFile):
    def __init__(self, file: str, data: dict = None) -> None:
        """Init function the song loader, itself an instance of the file loader
        with additioanl functionality to attempt to load individual song
        attributes.

        Args:
            file (str): The file to be loaded
            data (dict, optional): Data which has already been loaded but needs
            to be formatted as a loaded song. Defaults to None.
        """
        super().__init__("Songs", file)

        # Check if data was passed, and if not load the file.
        self.data = data if data else self.load()

        # Try to store the songs main attributes. Needs to be in a try except,
        # as if files are deleted / missing this will fail. 
        try:
            self.key = self.data["key"]
            self.name = self.data["title"]
            self.artist = self.data["subtitle"]
        except:
            self.key = None
            self.name = "Couldn't load song data"
            self.artist = " "

        # Try to store the songs track, which may fail if data was passed and
        # not a file when the object was intialised. 
        try:
            self.track = self.data["file"]
        except:
            self.track = None

        # Try to load the cover art of the song and store it as a QIcon. May
        # fail if the user is not connected to the internet. 
        try:
            request = requests.get(self.data["images"]["coverart"])
            pixmap = QPixmap()
            pixmap.loadFromData(request.content)

            self.icon = QIcon(pixmap)
        except:
            self.icon = QIcon()
