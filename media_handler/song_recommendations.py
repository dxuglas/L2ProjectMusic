import os
import random
from shazam_interface.recommendations import get_recommendations

DIRECTORY = os.path.expanduser(f'~/AppData/Local/Musi/Songs')

class SongRecommendations():
    def __init__(self) -> None:
        """The init function for song reccomendations, gets a list of songs
        avaliable. 
        """
        self.songs = []
        for song in os.listdir(DIRECTORY):
            if os.path.isfile(os.path.join(DIRECTORY, song)):
                self.songs.append(song)

    def from_library(self, count: int) -> list:
        """Gets song recomendations from the users library.

        Args:
            count (int): The number of songs to recommend

        Returns:
            list: The list of recommendations
        """
        recommendations = []

        # Check that enough songs are in the library, and if not cut back the
        # number of recommendations
        if count > len(self.songs):
            recommendations = random.sample(self.songs, len(self.songs))
            for i in range(count - len(self.songs)):
                recommendations.append(None)
        else:
            recommendations = random.sample(self.songs, count)
            
        return recommendations

    def from_shazam(self, key: str, count: int) -> list:
        """Gets song recommendations based on shazam similar songs.

        Args:
            key (str): The shazam key of the song recommendations are based on.
            count (int): The number of recommendations.

        Returns:
            list: The list of song recommendations.
        """ 

        # Try to get recommendations, fails if not internet access / shazam is
        # down.     
        try:
            recommendations = get_recommendations(key, count)
        except:
            recommendations = []
            for i in range(count):
                recommendations.append(None)

        return recommendations
