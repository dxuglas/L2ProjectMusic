import os
import random

DIRECTORY = os.path.expanduser(f'~/AppData/Local/Musi/Songs')

class SongRecomendations():
  def __init__(self) -> None:
    self.songs = []
    for song in os.listdir(DIRECTORY):
      if os.path.isfile(os.path.join(DIRECTORY, song)):
        self.songs.append(song)

  def from_library(self, count):
    recomendations = []

    for i in range(count):
      song = random.choice(self.songs)
      if song in recomendations:
        recomendations.append(None)
      else:
        recomendations.append(song)

    return recomendations

    

