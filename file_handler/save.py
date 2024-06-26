import json
import os

SAVE_DIRECTORY = os.path.expanduser(f'~/AppData/Local/Musi')

if not os.path.exists(SAVE_DIRECTORY):
  os.mkdir(SAVE_DIRECTORY)

class SaveFile():
  def __init__(self, name, data, path) -> None:

    self.path = os.path.expanduser(f'{SAVE_DIRECTORY}/{path}')

    if not os.path.exists(self.path):
      os.mkdir(self.path)

    with open(f'{self.path}/{name}.json', 'w') as f:
      json.dump(data, f)
    

class CreatePlaylistFile():
  def __init__(self, data) -> None:
    self.data = data
    self.name = self.data["name"]

    SaveFile(self.name, self.data, "Playlists")
