import argparse
import mpmath
import math
import re

from typing import Dict, Generator

from files import read_json, save_result
from constants import N, M, P_I


def frequency_bitwise_test(sequence: str) -> float:
    """
    This function implements a frequency bitwise test.

    Parameters:
        sequence: str
          The sequence for testing

    Returns:
        p_value: float
          Calculated p-value
    """
    s = sum(list(map(lambda x: 1 if x == "1" else -1, sequence))) / math.sqrt(N)
    p_value = math.erfc(s / math.sqrt(2))
    return p_value


def same_bits_test(sequence: str) -> float:
    """
    This function implements a test for the same consecutive bits.

    Parameters:
        sequence: str
          The sequence for testing

    Returns:
        p_value: float
          Calculated p-value
    """
    ones = sum(list(map(lambda x: 1 if x == "1" else 0, sequence))) / N
    if abs(ones - 0.5) < 2 / math.sqrt(N):
        changes = len([m.group(0)
                      for m in re.finditer(r"(\d)\1*", sequence)]) - 1
        p_value = math.erfc(abs(changes - 2 * N * ones * (1 - ones)) /
                            (2 * math.sqrt(2 * N) * ones * (1 - ones)))
    else:
        p_value = 0
    return p_value


def longest_sequence_test(sequence: str) -> float:
    """
    This function implements a test for the longest sequence of units in a block.

    Parameters:
        sequence: str
          The sequence for testing

    Returns:
        p_value: float
          Calculated p-value
    """
    all_longests = []
    for i in range(0, N - M + 1, M):
        sub_seq = [m.group(0)
                   for m in re.finditer(r"(\d)\1*", sequence[i:i+8])]
        all_longests.append(max([len(s) for s in sub_seq if '1' in s]))
    counter = {'<=1': 0, '=2': 0, '=3': 0, '>=4': 0}
    for value in all_longests:
        if value <= 1:
            counter['<=1'] += 1
        elif value == 2:
            counter['=2'] += 1
        elif value == 3:
            counter['=3'] += 1
        else:
            counter['>=4'] += 1
    hi_square = sum([((count - 16 * p)**2) / (16 * p)
                     for count, p in zip(counter.values(), P_I)])
    p_value = mpmath.gammainc(3/2, hi_square/2)
    return p_value


def sequences_test(sequences: Dict[str, str]) -> Generator[tuple[float,
                                                                 ...], None, None]:
    """
    This generator function tests sequences using three NIST tests

    Parameters:
        sequences: Dict[str, str]
          A dictionary where the key is the programming language with which the 
          sequence is obtained and the value is the sequence itself.

    Yields:
        fb_test, sb_test, ls_test: Generator[tuple[float,...], None, None]:
          Tests result for sequence
    """
    for sequence in sequences.values():
        fb_test = frequency_bitwise_test(sequence)
        sb_test = same_bits_test(sequence)
        ls_test = longest_sequence_test(sequence)
        yield fb_test, sb_test, ls_test


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sequences tests")
    parser.add_argument('settings', type=str, help='File with settings')
    args = parser.parse_args()
    settings = read_json(args.settings)
    if settings:
        sequences = read_json(settings.get('sequences'))
        path_to_result = settings.get('path_to_result')
        if sequences and path_to_result:
            for result, lang in zip(sequences_test(sequences), sequences):
                if save_result(path_to_result, result, lang, sequences[lang]):
                    print(f'Тест для последовательности на языке {lang} успешно завершен')
                else:
                    print('Некорректный путь для сохранения результата')
                    break
        else:
            print('Данные не найдены, проверьте имена параметров')
    else:
        print('Файл с параметрами не найден')
