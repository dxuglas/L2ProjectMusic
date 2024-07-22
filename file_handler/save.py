import json
import os

DIRECTORY = os.path.expanduser(f'~/AppData/Local/Musi')

class SaveFile():
  def __init__(self, name, data, path) -> None:

    self.path = os.path.expanduser(f'{DIRECTORY}/{path}')

    if not os.path.exists(self.path):
      os.mkdir(self.path)

    with open(f'{self.path}/{name}.json', 'w') as f:
      json.dump(data, f)
    

class CreatePlaylistFile():
  def __init__(self, data) -> None:
    self.data = data
    self.name = self.data["name"]

    SaveFile(self.name, self.data, "Playlists")
