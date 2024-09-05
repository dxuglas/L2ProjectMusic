"""This module is used to serve the user recommendations based on the Shazam
API.

Noah Douglas - 6/9/24
"""

import asyncio
from shazamio import Shazam
from .clean_data import clean


def get_recommendations(key: str, count: int) -> list:
    """This function handles interactions with the async shazam call for song
    recommendations, and also cleans the data before returning recommendations.

    Args:
        key (str): The key of a song to base recommendations off of.
        count (int): The number of songs to recommend.

    Returns:
        list: The list of song recommendations.
    """
    # Start an async loop and then query shazam inside it.
    loop = asyncio.get_event_loop()
    data = loop.run_until_complete(shazam_related_tracks(key, count))["tracks"]

    # Clean the sng data to remove all information that isn't wanted. 
    recommendations = []
    for track in data:
        recommendations.append(
            clean(track, ["title", "subtitle", "key", "images", "hub"]))

    return recommendations


async def shazam_related_tracks(key: str, count: int) -> list:
    """Querys the shazam api for song recommendations

    Args:
        key (str): The key to base recommendations on
        count (int): The number of recommendations

    Returns:
        list: The list of recommendations
    """

    shazam = Shazam()
    data = await shazam.related_tracks(track_id=key, limit=count)
    return data
