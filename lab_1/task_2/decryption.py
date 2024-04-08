import sys
import argparse

from files2 import read_json, read_text, save_text


def decryption(text: str, substitutions: str) -> None:
    """
    This function decrypts the text using the encryption key.

    Parameters:
        text: str
          Decrypted text
        substitutions: str
          The encryption key

    Returns:
        result: str
          Encrypted text
    """
    result = ''
    for letter in text:
        result += substitutions.get(letter)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Text decryption')
    parser.add_argument('settings', type=str, help='File with paths')
    args = parser.parse_args()
    settings = read_json(args.settings)
    if settings:
        try:
            path_to_encrypted = settings['encrypted']
            path_to_key = settings['encryption_key']
        except KeyError:
            print("Не удалось получить путь к тексту или ключу,\
                  проверьте имена параметров")
            sys.exit()
        else:
            text = read_text(path_to_encrypted)
            substitutions = read_json(path_to_key)
            if text is None or substitutions is None:
                print(f'Не удалось считать текст или ключ по адресу: {path_to_encrypted},\
                      {path_to_key}')
                sys.exit()
            result = decryption(text, substitutions)
        try:
            path_to_decrypted = settings['decrypted']
        except KeyError:
            print("Путь для сохранения не найден, проверьте имя параметра")
        else:
            if not save_text(path_to_decrypted, result):
                print(
                    f"Произошла ошибка при сохранени по адресу: {path_to_decrypted}")
    else:
        print("Файл с параметрами не найден")
