import json

def frequency_analysis(path_to_encrypted, path_to_frequency):
    with open(path_to_encrypted, 'r', encoding='utf-8') as f:
        text = f.read()
    result={}
    text_size = len(text)
    for letter in text:
        if letter in result:
            continue
        count = text.count(letter)
        result[letter] = count/text_size
    sorted_result={}
    sorted_key = sorted(result, key = result.get, reverse=True)
    for key in sorted_key:
        sorted_result[key] = result.get(key)

    with open(path_to_frequency, 'w', encoding='utf-8') as json_file:
        json.dump(sorted_result, json_file, ensure_ascii=False)

def decryption(path_to_encrypted, path_to_key, path_to_decrypted):
    with open(path_to_encrypted, 'r', encoding='utf-8') as f:
        text = f.read()
    with open(path_to_key, 'r', encoding='utf-8') as json_file:
        sub = json.load(json_file)
    result = ''
    for letter in text:
        result+=sub.get(letter)
    with open(path_to_decrypted, 'w', encoding='utf-8') as f:
        f.write(result)

def main() -> None:
    with open('lab_1/task_2/settings.json', 'r', encoding='utf-8') as json_file:
        settings = json.load(json_file)
    #frequency_analysis(settings['encrypted'], settings['frequency_encrypted'])
    decryption(settings['encrypted'], settings['encryption_key'], settings['decrypted'])
