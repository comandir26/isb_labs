import sys
import argparse
from typing import Dict

from files1 import read_json, read_text, save_text, save_json
from constants import LETTERS, DATA, MARKS


def substitution_cipher(keyword: str,
                        text: str) -> tuple[str, Dict[str, str]]:
    """
    This function encrypts the text by substitution.

    Parameters:
        keyword: str
          Substitution key
        text: str
          The original text

    Returns:
        result: str
          Encrypted text
        substitutions: Dict[str, str]
          Encryption key
    """
    substitutions = {}
    substitutions |= MARKS
    keyword = keyword * int(len(text)/len(keyword)) + \
        keyword[:len(text) % len(keyword)]
    result = ''
    for text_letter, key_letter in zip(text, keyword):
        if text_letter.upper() in substitutions:
            result += substitutions.get(text_letter.upper())
            continue
        count = DATA.get(text_letter.upper()) + DATA.get(key_letter.upper())
        if count > 32:
            count -= 32
        result += LETTERS[count-1]
        substitutions[text_letter.upper()] = LETTERS[count-1].upper()
    return result, substitutions


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Text encryption')
    parser.add_argument('keyword', type=str, help='Substitution key')
    parser.add_argument('settings', type=str, help='File with paths')
    args = parser.parse_args()
    settings = read_json(args.settings)
    if settings:
        try:
            path_to_original = settings["original"]
        except KeyError:
            print("Не удалось получить путь к тексту, проверьте имя параметра")
            sys.exit()
        else:
            text = read_text(path_to_original)
            if text is None:
                print(
                    f"Не удалось считать текст по адресу: {path_to_original}")
                sys.exit()
            result, encryption_key = substitution_cipher(args.keyword, text)
        try:
            path_to_encrypted = settings["encrypted"]
            path_to_key = settings["encryption_key"]
        except KeyError:
            print("Пути для сохранения не найдены, проверьте имена параметров")
        else:
            if not save_text(path_to_encrypted, result) or not save_json(path_to_key,
                                                                         encryption_key):
                print(f'Произошла ошибка при сохранении по адресам: {path_to_encrypted},\
                      {path_to_key}')
    else:
        print("Файл с параметрами не найден")
