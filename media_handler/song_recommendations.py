import os
import random
from shazam_interface.recommendations import get_recommendations

DIRECTORY = os.path.expanduser(f'~/AppData/Local/Musi/Songs')


class SongRecommendations():
    def __init__(self) -> None:
        self.songs = []
        for song in os.listdir(DIRECTORY):
            if os.path.isfile(os.path.join(DIRECTORY, song)):
                self.songs.append(song)

    def from_library(self, count):
        recommendations = []

        if count > len(self.songs):
            recommendations = random.sample(self.songs, len(self.songs))
            for i in range(count - len(self.songs)):
                recommendations.append(None)
        else:
            recommendations = random.sample(self.songs, count)

        return recommendations

    def from_shazam(self, key, count):
        try:
            recommendations = get_recommendations(key, count)
        except:
            recommendations = []
            for i in range(count):
                recommendations.append(None)

        return recommendations
