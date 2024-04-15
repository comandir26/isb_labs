import argparse
import math
import re

import mpmath

from files import read_json
from constants import N, M, P_I


def frequency_bitwise_test(sequence: list) -> None:
    p_value = math.erfc((sum(list(map(lambda x: 1 if x == "1" else -1, sequence))) /
                         math.sqrt(N)) / math.sqrt(2))
    print(p_value)


def same_bits_test(sequence: list) -> None:
    ones = sum(list(map(lambda x: 1 if x == "1" else 0,
                        sequence))) / N
    if abs(ones - 0.5) < 2/math.sqrt(N):
        changes = sum([1 if sequence[i] != sequence[i + 1]
                      else 0 for i in range(N - 1)])
        p_value = math.erfc(abs(changes - 2 * N * ones * (1 - ones)) /
                            (2 * math.sqrt(2 * N) * ones * (1 - ones)))
    else:
        p_value = 0
    print(p_value)


def longest_sequence_test(sequence: list) -> None:
    all_longests = []
    for i in range(0, N - M + 1, M):
        sub_seq = [m.group(0) for m in re.finditer(r"(\d)\1*", sequence[i:i+8])]
        all_longests.append(max([len(s) for s in sub_seq if '1' in s]))
    counter = {'<=1': 0, '=2': 0, '=3': 0, '>=4': 0}
    for value in all_longests:
        if value <= 1:
            counter['<=1']+=1
        elif value == 2:
            counter['=2']+=1
        elif value == 3:
            counter['=3']+=1
        else:
            counter['>=4']+=1
    hi_stat = sum([ ((count - 16 * p)**2) / (16 * p) for count, p in zip(counter.values(), P_I)])
    print(f'hi_stat = {hi_stat}')
    print(f'p_value = {mpmath.gammainc(1.5, hi_stat/2)}')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sequences tests")
    parser.add_argument('settings', type=str, help='File with sequences')
    args = parser.parse_args()
    settings = read_json(args.settings)
    if settings:
        #frequency_bitwise_test(settings['c'])
        #frequency_bitwise_test(settings['java'])
        #same_bits_test(settings['c'])
        #same_bits_test(settings['java'])
        longest_sequence_test(settings['c'])
        longest_sequence_test(settings['java'])
    else:
        print('Файл с параметрами не найден')
