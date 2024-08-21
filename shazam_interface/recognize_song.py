import asyncio
from shazamio import Shazam

from .clean_data import clean


def recognise(file: str) -> dict:
    """Recognise a song using the shazam api. Handles interfacing with the async
    shazam function and also cleans the data to remove unwanted attributes.

    Args:
        file (str): The file that needs to be recognised.

    Returns:
        dict: The song data from shazam.
    """
    loop = asyncio.get_event_loop()
    data = loop.run_until_complete(get_song_data(file))
    cleaned_data = clean(data, ["title", "subtitle", "key", "images"])
    return cleaned_data


async def get_song_data(file: str) -> dict:
    """The async shazam function, which gets the information about a song based
    on it's file. 

    Args:
        file (str): The file of the song.

    Returns:
        dict: The song data.
    """
    shazam = Shazam()
    data = await shazam.recognize(file)
    return data["track"]
