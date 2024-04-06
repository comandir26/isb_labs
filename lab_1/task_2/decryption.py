import sys
import argparse

import files2 as f


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
    settings = f.read_json(args.settings)
    if settings:
        try:
            path_to_encrypted = settings['encrypted']
            path_to_key = settings['encryption_key']
        except KeyError:
            print("Параметры по заданным путям не найдены")
            sys.exit()
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            sys.exit()
        else:
            text = f.read_text(path_to_encrypted)
            substitutions = f.read_json(path_to_key)
            result = decryption(text, substitutions)
    else:
        print("Файл с параметрами не найден")
        sys.exit()
    try:
        path_to_decrypted = settings['decrypted']
    except KeyError:
        print("Путь для сохранения не найден, проверьте имя параметра")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    else:
        f.save_text(path_to_decrypted, result)     