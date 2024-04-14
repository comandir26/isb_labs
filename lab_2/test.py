import argparse
import math

from files import read_json


def frequency_bitwise_test(sequence: list) -> None:
    p_value = math.erfc((sum(list(map(lambda x: 1 if x == "1" else -1, sequence))) /
                         math.sqrt(len(sequence))) / math.sqrt(2))
    print(p_value)


def same_bits_test(sequence: list) -> None:
    ones = sum(list(map(lambda x: 1 if x == "1" else 0,
                        sequence))) / math.sqrt(len(sequence))
    if abs(ones - 0.5) < 2/math.sqrt(len(sequence)):
        changes = sum([1 if sequence[i] != sequence[i + 1]
                      else 0 for i in range(len(sequence) - 1)])
        p_value = math.erfc(abs(changes - 2 * len(sequence) * ones * (1 - ones)) /
                            (2 * math.sqrt(2 * len(sequence)) * ones * (1 - ones)))
    else:
        p_value = 0
    print(p_value)


def longest_sequence_test(sequence: list) -> None:
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sequences tests")
    parser.add_argument('settings', type=str, help='File with sequences')
    args = parser.parse_args()
    settings = read_json(args.settings)
    if settings:
        frequency_bitwise_test(settings['c'])
        frequency_bitwise_test(settings['java'])
        same_bits_test(settings['c'])
        same_bits_test(settings['java'])
    else:
        print('Файл с параметрами не найден')
