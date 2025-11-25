# based on https://github.com/barrust/pyspellchecker/blob/5de51fc22ceba53eacfcaf386e5c08057f461236/scripts/build_dictionary.py

import json
from collections import Counter
import re
import os

WORD_REGEX = r'\b[абвгдежзийклмнопрстуфхцчшщъыьэюяёіғңҷӧӱ-]+\b'
KHAKAS_LETTERS = "абвгдежзийклмнопрстуфхцчшщъыьэюяёіғңҷӧӱ"
KHAKAS_VOWELS = "аеиоуыэюяёіӧӱ"
MINIMUM_FREQUENCY = 50


def export_word_frequency(filepath, word_frequency):
    """Export a word frequency as a json object

    Args:
        filepath (str):
        word_frequency (Counter):
    """
    with open(filepath, "w") as f:
        json.dump(word_frequency, f, indent="", sort_keys=True, ensure_ascii=False)


def build_word_frequency_custom(filepath, output_path):
    word_frequency = Counter()
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            words = re.findall(WORD_REGEX, line.lower())
            word_frequency.update(words)

    export_word_frequency(output_path, word_frequency)

    return word_frequency


def clean_khakas(word_frequency, filepath_exclude=None, filepath_include=None):
    # based on `clean_russian` https://github.com/barrust/pyspellchecker/blob/5de51fc22ceba53eacfcaf386e5c08057f461236/scripts/build_dictionary.py#L666
    letters = set(KHAKAS_LETTERS)

    # remove words with invalid characters
    invalid_chars = list()
    for key in word_frequency:
        kl = set(key)
        if kl.issubset(letters):
            continue
        invalid_chars.append(key)
    for misfit in invalid_chars:
        word_frequency.pop(misfit)

    # remove words without a vowel
    no_vowels = list()
    vowels = set(KHAKAS_VOWELS)
    for key in word_frequency:
        if vowels.isdisjoint(key):
            no_vowels.append(key)
    for misfit in no_vowels:
        word_frequency.pop(misfit)

    # remove small numbers
    small_frequency = list()
    for key in word_frequency:
        if word_frequency[key] <= MINIMUM_FREQUENCY:
            small_frequency.append(key)
    for misfit in small_frequency:
        word_frequency.pop(misfit)

    # remove flagged misspellings
    if os.path.exists(filepath_exclude):
        with open(filepath_exclude, 'r', encoding='utf-8') as f:
            for line in f:
                exclude_words = re.findall(WORD_REGEX, line.lower())
                for exclude_word in exclude_words:
                    if exclude_word in word_frequency:
                        word_frequency.pop(exclude_word)

    # Add known missing words back in
    if os.path.exists(filepath_include):
        with open(filepath_exclude, 'r', encoding='utf-8') as f:
            for line in f:
                include_words = re.findall(WORD_REGEX, line.lower())
                for include_word in include_words:
                    if include_word in word_frequency:
                        print("{} is already found in the dictionary! Skipping!".format(include_word))
                    else:
                        word_frequency[include_word] = MINIMUM_FREQUENCY

    return word_frequency


def main():
    pass


if __name__ == '__main__':
    main()