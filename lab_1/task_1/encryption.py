import json
import argparse


letters = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"


def substitution_cipher(keyword: str, path_to_original: str,
                        path_to_result: str, path_to_key: str) -> None:
    """
    This function encrypts the text by substitution, 
    saves the encrypted text and the encryption key.

    Parameters:
        keyword: str
          Substitution key
        path_to_original: str
          The path to the original text
        path_to_result: str
          The path to save the encrypted text
        path_to_key: str
          The path to save the encryption key

    Returns:
        None
    """
    numbers = range(1, len(letters) + 1)
    data = dict(zip(letters, numbers))
    substitutions = {}
    with open(path_to_original, 'r', encoding='utf-8') as f:
        text = f.read()
    keyword = keyword * int(len(text)/len(keyword)) + \
        keyword[:len(text) % len(keyword)]
    result = ''
    for text_letter, key_letter in zip(text, keyword):
        if text_letter.upper() in substitutions:
            result += substitutions.get(text_letter.upper())
            continue
        if text_letter.upper() not in letters:
            result += text_letter
            continue
        count = data.get(text_letter.upper()) + data.get(key_letter.upper())
        if count > 32:
            count -= 32
        result += letters[count-1]
        substitutions[text_letter.upper()] = letters[count-1].upper()
    with open(path_to_result, 'w', encoding='utf-8') as f:
        f.write(result)
    with open(path_to_key, 'w', encoding='utf-8') as json_file:
        json.dump(substitutions, json_file, ensure_ascii=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Text encryption')
    parser.add_argument('keyword', type=str, help='Substitution key')
    parser.add_argument('settings', type=str, help='File with paths')
    args = parser.parse_args()
    with open(args.settings, 'r', encoding='utf-8') as json_file:
        settings = json.load(json_file)
    substitution_cipher(args.keyword, settings['original'],
                        settings['encrypted'], settings['encryption_key'])
