import json
import os

DIRECTORY = os.path.expanduser(f'~/AppData/Local/Musi')

class Playlists():
  def __init__(self) -> None:
    self.dir = fr"{DIRECTORY}/Playlists/"
    self.playlists = []

  def load(self):
    for file in os.listdir(self.dir):
      with open(fr"{self.dir}/{file}", 'r') as f:
        self.playlists.append(json.load(f))
    
    return self.playlists