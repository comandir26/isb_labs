import json

letters = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"


def substitution_cipher(keyword, path_to_original, path_to_result, path_to_encryption_key) -> None:
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
            result+=substitutions.get(text_letter.upper())
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
    with open(path_to_encryption_key, 'w', encoding='utf-8') as json_file:
        json.dump(substitutions, json_file, ensure_ascii=False)


def main() -> None:
    with open('lab_1/task_1/settings.json', 'r', encoding='utf-8') as json_file:
        settings = json.load(json_file)
    substitution_cipher(settings['keyword'], settings['original'],
                        settings['encrypted'], settings['encryption_key'])
