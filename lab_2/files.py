import json

from typing import Optional, Dict


def read_json(path_to_data: str) -> Optional[Dict[str, str]]:
    """
    This function reads data in json format at the specified path.

    Parameters:
        path_to_data: str
          The path to the data

    Returns:
        data: Optional[Dict[str, str]]
          The read data or None
    """
    try:
        with open(path_to_data, 'r') as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        data = None
    finally:
        return data