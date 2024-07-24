def clean(data, keys):
  clean = {}

  for key in keys:
    if isinstance(key, tuple):
      clean[key[1]] = data["images"]["coverart"]
    else:
      clean[key] = data[key]

  return clean