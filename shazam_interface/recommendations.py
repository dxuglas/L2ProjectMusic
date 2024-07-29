import asyncio
from shazamio import Shazam

from .clean_data import clean

def get_recommendations(key, count):
  loop = asyncio.get_event_loop()
  data = loop.run_until_complete(get_recommendations_async(key, count))["tracks"]

  recommendations = []
  for track in data:
    recommendations.append(clean(track, ["title", "subtitle", "key", "images"]))

  return recommendations

async def get_recommendations_async(key, count):
  shazam = Shazam()
  data = await shazam.related_tracks(track_id=key, limit=count)
  return data