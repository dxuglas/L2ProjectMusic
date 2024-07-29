import json
import os

DIRECTORY = os.path.expanduser(f'~/AppData/Local/Musi')

if not os.path.exists(DIRECTORY):
  os.mkdir(DIRECTORY)
  os.mkdir(fr"{DIRECTORY}/Playlists/")
  os.mkdir(fr"{DIRECTORY}/Songs/")

class Playlists():
  def __init__(self) -> None:
    self.dir = fr"{DIRECTORY}/Playlists/"
    self.playlists = []

    if not os.path.exists(self.dir):
      os.mkdir(self.dir)

  def load(self):
    for file in os.listdir(self.dir):
      with open(fr"{self.dir}/{file}", 'r') as f:
        self.playlists.append(json.load(f))
    
    return self.playlists
  
class LoadFile():
  def __init__(self, dir, file) -> None:
    self.dir = fr"{DIRECTORY}/{dir}/"
    self.file = None

  def load(self):
    with open(fr"{self.dir}/{self.file}", 'r') as f:
      self.file = f

    return self.file
  
class LoadSong(LoadFile):
  def __init__(self, file) -> None:
    super().__init__("Songs", file)
