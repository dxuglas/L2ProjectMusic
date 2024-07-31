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
    self.dir = "Playlists"
    self.playlists = []

  def load(self):
    for file in os.listdir(fr"{DIRECTORY}/{self.dir}"):
      self.playlists.append(LoadFile(self.dir, file).load())
    
    return self.playlists
  
class Songs():
  def __init__(self) -> None:
    self.dir = "Songs"
    self.songs = []

  def load(self):
    for file in os.listdir(fr"{DIRECTORY}/{self.dir}"):
      
      self.songs.append(LoadSong(file))
    
    return self.songs
  
class LoadFile():
  def __init__(self, dir, file) -> None:
    self.dir = fr"{DIRECTORY}/{dir}/"
    self.file = file

    if not os.path.exists(self.dir):
      os.mkdir(self.dir)

  def load(self):
    try:
      with open(fr"{self.dir}/{self.file}", 'r') as f:
        self.file = json.load(f)
    except:
      self.file = None

    return self.file

class LoadSong(LoadFile):
  def __init__(self, file, data = None) -> None:
    super().__init__("Songs", file)

    self.data = data if data else self.load()

    self.key = self.data["key"]
    self.name = self.data["title"]
    self.artist = self.data["subtitle"]
    
    try:
      request = requests.get(self.data["images"]["coverart"])
      pixmap = QPixmap()
      pixmap.loadFromData(request.content)

      self.icon = QIcon(pixmap)
    except:
      self.icon = QIcon()
