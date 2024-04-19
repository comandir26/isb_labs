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


def save_result(path_to_save: str, result: tuple[float, ...], 
                lang: str, seq: str) -> bool:
    """
    This function saves the result of the tests in the specified path.

    Parameters:
        path_to_save: str
          The path to save the text
        result: tuple[float, ...]
          The result of three NIST tests
        lang: str
          The programming language with which the sequence is obtained
        seq: str
          The sequence itself

    Returns:
        saved: bool
          An indicator showing whether the result has been saved
    """
    saved = True
    output = f'{lang}: {seq}\nfrequency_test: {result[0]}\nsame_bits_test: '\
                f'{result[1]}\nlongest_seq_test: {result[2]}\n\n'
    try:
        with open(path_to_save, 'a', encoding='utf-8') as f:
            f.write(output)
    except FileNotFoundError:
        saved = False
    finally:
        return saved
