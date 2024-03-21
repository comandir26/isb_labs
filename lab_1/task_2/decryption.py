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

def decoding(path_to_encrypted, path_to_freq_encrypted, path_to_freq_alphabet, path_to_decrypted):
    with open(path_to_encrypted, 'r', encoding='utf-8') as f:
        text = f.read()
    with open(path_to_freq_encrypted, 'r', encoding='utf-8') as json_file:
        freq_encrypted = json.load(json_file)
    with open(path_to_freq_alphabet, 'r', encoding='utf-8') as json_file:
        freq_alphabet = json.load(json_file)
    for encrypt, decrypt in zip(freq_encrypted.keys(), freq_alphabet.keys()):
        text = text.replace(encrypt, decrypt)
        print(text)
    
def main() -> None:
    with open('lab_1/task_2/settings.json', 'r', encoding='utf-8') as json_file:
        settings = json.load(json_file)
    #frequency_analysis(settings['encrypted'], settings['frequency_encrypted'])
    decoding(settings['encrypted'], settings['frequency_encrypted'], settings['frequency_alphabet'], settings['decrypted'])