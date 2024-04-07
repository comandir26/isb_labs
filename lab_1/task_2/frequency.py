import sys
import argparse
from typing import Dict

import files2 as f


def frequency_analysis(text: str) -> Dict[str, float]:
    """
    A function for performing frequency analysis of text

    Parameters:
        text: str
          Text for analysis

    Returns:
        sorted_result: Dict[str, float]
          A dictionary where the key is the symbol and the value is the frequency
    """
    result = {}
    text_size = len(text)
    for letter in text:
        if letter in result:
            continue
        count = text.count(letter)
        result[letter] = count/text_size
    sorted_result = {}
    sorted_key = sorted(result, key=result.get, reverse=True)
    for key in sorted_key:
        sorted_result[key] = result.get(key)
    return sorted_result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Frequency analysis')
    parser.add_argument('settings', type=str, help='File with paths')
    args = parser.parse_args()
    settings = f.read_json(args.settings)
    if settings:
        try:
            path_to_text = settings['encrypted']
        except KeyError:
            print("Не удалось получить путь к тексту, проверьте имя параметра")
            sys.exit()
        else:
            text = f.read_text(path_to_text)
            if text is None:
                print(f"Не удалось считать текст по адресу: {path_to_text}")
                sys.exit()
            frequency = frequency_analysis(text)
        try:
            path_to_frequency = settings['frequency_encrypted']
        except KeyError:
            print("Путь для сохранения не найден, проверьте имя параметра")
        else:
            if not f.save_json(path_to_frequency, frequency):
                print(f'Произошла ошибка при сохранении по адресу: {path_to_frequency}')
    else:
        print("Файл с параметрами не найден")
