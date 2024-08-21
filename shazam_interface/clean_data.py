def clean(data: dict, keys: list) -> dict:
    """Cleans a dictionary to remove all unwanted keys.

    Args:
        data (dict): The dict to be cleaned
        keys (list): The keys which are wanted

    Returns:
        dict: The resulting cleaned dict.
    """
    cleaned = {}

    for key in keys:
        cleaned[key] = data[key]

    return cleaned
