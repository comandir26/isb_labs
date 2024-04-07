import sys
import argparse
from typing import Dict

import files1 as f
from constants import letters


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
    numbers = range(1, len(letters) + 1)
    data = dict(zip(letters, numbers))
    substitutions = {",": ",", ".": ".", "-": "-", "?": "?", "!": "!", " ": " "}
    keyword = keyword * int(len(text)/len(keyword)) + \
        keyword[:len(text) % len(keyword)]
    result = ''
    for text_letter, key_letter in zip(text, keyword):
        if text_letter.upper() in substitutions:
            result += substitutions.get(text_letter.upper())
            continue
        count = data.get(text_letter.upper()) + data.get(key_letter.upper())
        if count > 32:
            count -= 32
        result += letters[count-1]
        substitutions[text_letter.upper()] = letters[count-1].upper()
    return result, substitutions


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Text encryption')
    parser.add_argument('keyword', type=str, help='Substitution key')
    parser.add_argument('settings', type=str, help='File with paths')
    args = parser.parse_args()
    settings = f.read_json(args.settings)
    if settings:
        try:
            path_to_original = settings["original"]
        except KeyError:
            print("Не удалось получить путь к тексту, проверьте имя параметра")
            sys.exit()
        else:
            text = f.read_text(path_to_original)
            if text is None:
                print(f"Не удалось считать текст по адресу: {path_to_original}")
                sys.exit()
            result, encryption_key = substitution_cipher(args.keyword, text)
        try:
            path_to_encrypted = settings["encrypted"]
            path_to_key = settings["encryption_key"]
        except KeyError:
            print("Пути для сохранения не найдены, проверьте имена параметров")
        else:
            if not f.save_text(path_to_encrypted, result) or not f.save_json(path_to_key, 
                                                                      encryption_key):
                print(f'Произошла ошибка при сохранении по адресам: {path_to_encrypted},\
                      {path_to_key}')
    else:
        print("Файл с параметрами не найден")