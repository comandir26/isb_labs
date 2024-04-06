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
            print("Текст по заданному пути не найден")
            sys.exit()
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            sys.exit()
        else:
            text = f.read_text(path_to_text)
            frequency = frequency_analysis(text)
    else:
        print("Файл с параметрами не найден")
        sys.exit()
    try:
        path_to_frequency = settings['frequency_encrypted']
    except KeyError:
        print("Путь для сохранения не найден, проверьте имя параметра")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    else:
         f.save_json(path_to_frequency, frequency)
