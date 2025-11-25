# based on https://github.com/barrust/pyspellchecker/blob/5de51fc22ceba53eacfcaf386e5c08057f461236/scripts/build_dictionary.py

import json
from collections import Counter
import re
import os

KHAKAS_LETTERS_AND_HYPHEN = "абвгдежзийклмнопрстуфхцчшщъыьэюяёіғңҷӧӱ-"
KHAKAS_VOWELS = "аеиоуыэюяёіӧӱ"
WORD_REGEX = r'\b[абвгдежзийклмнопрстуфхцчшщъыьэюяёіғңҷӧӱ-]{2,}\b'  # слова от 2-х букв
MINIMUM_FREQUENCY = 10


def export_word_frequency(filepath, word_frequency):
    """Export a word frequency as a json object

    Args:
        filepath (str):
        word_frequency (Counter):
    """
    with open(filepath, "w", encoding='utf-8') as f:
        json.dump(word_frequency, f, indent="", sort_keys=True, ensure_ascii=False)


def build_word_frequency_custom(filepath, output_path):
    word_frequency = Counter()
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            words = re.findall(WORD_REGEX, line.lower())
            word_frequency.update(words)

    export_word_frequency(output_path, word_frequency)

    return word_frequency


def include_exclude_words(word_frequency, include_filepaths=None, exclude_filepaths=None):
    # remove flagged misspellings
    if exclude_filepaths:
        for exclude_filepath in exclude_filepaths:
            if os.path.exists(exclude_filepath):
                with open(exclude_filepath, 'r', encoding='utf-8') as f:
                    for line in f:
                        exclude_words = re.findall(WORD_REGEX, line.lower())
                        for exclude_word in exclude_words:
                            if exclude_word in word_frequency:
                                word_frequency.pop(exclude_word)

    # Add known missing words back in
    if include_filepaths:
        for include_filepath in include_filepaths:
            if os.path.exists(include_filepath):
                with open(include_filepath, 'r', encoding='utf-8') as f:
                    for line in f:
                        include_words = re.findall(WORD_REGEX, line.lower())
                        for include_word in include_words:
                            if include_word in word_frequency:
                                word_frequency[include_word] = max(MINIMUM_FREQUENCY, word_frequency[include_word])
                            else:
                                word_frequency[include_word] = MINIMUM_FREQUENCY

    return word_frequency


def clean_khakas(word_frequency):
    # based on `clean_russian` https://github.com/barrust/pyspellchecker/blob/5de51fc22ceba53eacfcaf386e5c08057f461236/scripts/build_dictionary.py#L666

    letters = set(KHAKAS_LETTERS_AND_HYPHEN)

    no_valid_words = list()
    for key in word_frequency:
        if key[0] == '-' or key[-1] == '-':
            no_valid_words.append(key)
    for misfit in no_valid_words:
        word_frequency.pop(misfit)

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
        if word_frequency[key] < MINIMUM_FREQUENCY:
            small_frequency.append(key)
    for misfit in small_frequency:
        word_frequency.pop(misfit)

    return word_frequency


def export_misfit_words(misfit_filepath, word_freq_filepath, word_frequency):
    with open(word_freq_filepath, 'r', encoding='utf-8') as f:
        source_word_frequency = json.load(f)

    source_words = set(source_word_frequency.keys())
    final_words = set(word_frequency.keys())

    misfitted_words = source_words.difference(final_words)
    misfitted_words = sorted(list(misfitted_words))

    misfitted_word_frequency = Counter({word: source_word_frequency[word] for word in misfitted_words})
    print('Число слов, не попавших в словарь :', len(misfitted_word_frequency))
    print('Топ 10 слов, не попавших в словарь :', misfitted_word_frequency.most_common(10))
    export_word_frequency(misfit_filepath, misfitted_word_frequency)


def main():
    json_full_path = './data/khakas_uchebniki_word_dict_frequency_full.json'
    json_path = './data/khakas_uchebniki_word_dict_frequency.json'
    file_path = './data/khakas_uchebniki.txt'
    misfit_filepath = './data/khakas_uchebniki_word_dict_frequency_misfit.json'
    include_filepaths = ['./data/khakas_defis_words_custom.txt',
                         './data/khakas_defis_words_dict_hrs_new34.txt']
    word_frequency = build_word_frequency_custom(file_path, json_full_path)
    word_frequency = include_exclude_words(word_frequency, include_filepaths=include_filepaths)
    word_frequency = clean_khakas(word_frequency)

    print('Число слов в словаре :', len(word_frequency))
    print('Топ 10 частых слово :', word_frequency.most_common(10))
    print('\n\n')

    export_word_frequency(json_path, word_frequency)

    if misfit_filepath:
        export_misfit_words(misfit_filepath, json_full_path, word_frequency)


if __name__ == '__main__':
    main()
