import json
from typing import Dict, Optional


def read_text(path_to_text: str) -> Optional[str]:
    """
    This function reads the text in the specified path.

    Parameters:
        path_to_text: str
          The path to the text

    Returns:
        text: str
          The read text
    """
    with open(path_to_text, 'r', encoding='utf-8') as f:
            text = f.read()
            return text

def save_text(path_to_save: str, text: str) -> None:
    """
    This function saves the text in the specified path.

    Parameters:
        path_to_save: str
          The path to save the text
        text: str
          Text to save

    Returns:
        None
    """
    with open(path_to_save, 'w', encoding='utf-8') as f:
        f.write(text)


def read_json(path_to_data: str) -> Optional[Dict[str, str]]:
    """
    This function reads data in json format at the specified path.

    Parameters:
        path_to_data: str
          The path to the data

    Returns:
        data: Dict[str, str]
          The read data
    """
    with open(path_to_data, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        return data


def save_json(path_to_save: str, data: Dict[str, str]) -> None:
    """
    This function saves data in json format at the specified path.

    Parameters:
        path_to_save: str
          The path to save the data
        data: Dict[str, str]
          Data to save

    Returns:
        None
    """
    with open(path_to_save, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False)
