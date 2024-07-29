import asyncio
from shazamio import Shazam

from .clean_data import clean

def get_recomendations(key):
  loop = asyncio.get_event_loop()
  data = loop.run_until_complete(get_recomendations_async(key))
  cleaned_data = clean(data, ["title", "subtitle", "key", "images"])
  return cleaned_data

async def get_recomendations_async(key):
  shazam = Shazam()
  data = await shazam.related_tracks(track_id=key, limit=5)
  return data