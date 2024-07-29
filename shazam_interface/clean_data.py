
def clean(data, keys):
  cleaned = {}

  for key in keys:
    cleaned[key] = data[key]

  return cleaned