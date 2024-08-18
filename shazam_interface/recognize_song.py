import asyncio
from shazamio import Shazam

from .clean_data import clean


def recognise(file):
    loop = asyncio.get_event_loop()
    data = loop.run_until_complete(get_song_data(file))
    cleaned_data = clean(data, ["title", "subtitle", "key", "images"])
    return cleaned_data


async def get_song_data(file):
    shazam = Shazam()
    data = await shazam.recognize(file)
    return data["track"]
