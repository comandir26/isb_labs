import json
import argparse


def decryption(path_to_encrypted: str, path_to_key: str, path_to_decrypted: str) -> None:
    """
    This function decrypts the text using the encryption key,
    saves the decrypted text.

    Parameters:
        path_to_encrypted: str
          The path to the encrypted text
        path_to_key: str
          The path to the encryption key
        path_to_decrypted: str
          The path to save the result of decryption

    Returns:
        None
    """
    with open(path_to_encrypted, 'r', encoding='utf-8') as f:
        text = f.read()
    with open(path_to_key, 'r', encoding='utf-8') as json_file:
        sub = json.load(json_file)
    result = ''
    for letter in text:
        result += sub.get(letter)
    with open(path_to_decrypted, 'w', encoding='utf-8') as f:
        f.write(result)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Text decryption')
    parser.add_argument('settings', type=str, help='File with paths')
    args = parser.parse_args()
    with open(args.settings, 'r', encoding='utf-8') as json_file:
        settings = json.load(json_file)
    decryption(settings['encrypted'], settings['encryption_key'],
               settings['decrypted'])
