import json
import os

DIRECTORY = os.path.expanduser(f'~/AppData/Local/Musi')


class SaveFile():
    def __init__(self, name: str, data: str, path: str) -> None:
        """Saves a file to the users save directory.

        Args:
            name (str): The name of the file to be saved
            data (str): The data to store in the file
            path (str): The path the file is to be saved at
        """

        self.path = os.path.expanduser(f'{DIRECTORY}/{path}')

        if not os.path.exists(self.path):
            os.mkdir(self.path)

        with open(f'{self.path}/{name}.json', 'w') as f:
            json.dump(data, f)


class CreatePlaylistFile():
    def __init__(self, data: dict) -> None:
        """Save a playlist file

        Args:
            data (dict): The playlist data to be saved.
        """

        self.data = data
        self.name = self.data["name"]

        SaveFile(self.name, self.data, "Playlists")


class CreateSongFile():
    def __init__(self, data: dict) -> None:
        """Saves a song file

        Args:
            data (dict): The song data to be saved. 
        """
        
        self.data = data

        self.name = self.data["key"]

        SaveFile(self.name, self.data, "Songs")
