import json
import argparse


def frequency_analysis(path_to_encrypted: str, path_to_frequency: str) -> None:
    """
    A function for performing frequency analysis of text

    Parameters:
        path_to_encrypted: str
          The path to the text
        path_to_frequency: str
          The path to save the result of analysis

    Returns:
        None
    """
    with open(path_to_encrypted, 'r', encoding='utf-8') as f:
        text = f.read()
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
    with open(path_to_frequency, 'w', encoding='utf-8') as json_file:
        json.dump(sorted_result, json_file, ensure_ascii=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Frequency analysis')
    parser.add_argument('settings', type=str, help='File with paths')
    args = parser.parse_args()
    with open(args.settings, 'r', encoding='utf-8') as json_file:
        settings = json.load(json_file)
    frequency_analysis(settings['encrypted'], settings['frequency_encrypted'])
