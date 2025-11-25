import pandas as pd
from spellchecker import SpellChecker
import re

WORD_REGEX = r'\b[абвгдежзийклмнопрстуфхцчшщъыьэюяёіғңҷӧӱ-]{2,}\b'  # слова от 2-х букв
spell_checker = SpellChecker(language=None,
                             local_dictionary='./data/khakas_uchebniki_word_dict_frequency.json')


def get_correction_candidates(sent):
    words_to_check = re.findall(WORD_REGEX, sent.lower())
    misspelled = spell_checker.unknown(words_to_check)

    if not misspelled:
        return None

    results = []
    for word in misspelled:
        correction = spell_checker.correction(word)
        candidates = spell_checker.candidates(word)

        if not candidates:
            continue

        # Create a list of candidates excluding the main correction
        other_candidates = [c for c in candidates if c != correction]

        # Format the result string
        result = f"Слово с ошибкой: '{word}'"
        if correction:
            result += f"\nНаиболее вероятное исправление: '{correction}'"

        if len(other_candidates) > 0:
            result += f"\nДругие варианты: {', '.join(f"'{c}'" for c in other_candidates[:5])}"

        results.append(result)

    return "\n\n".join(results) if results else None


def main():
    path = 'data/example.csv'
    df = pd.read_csv(path)[:25]

    # Add progress counter
    total_rows = len(df)
    print(f"Processing {total_rows} rows...")

    results = []
    for idx, row in df.iterrows():
        # Show progress
        if idx % 10 == 0 or idx == total_rows - 1:
            print(f"Processing row {idx + 1}/{total_rows}...")

        result = get_correction_candidates(row['Хакасский'])
        results.append(result)

    df['misspelled_correction_candidates'] = results
    output_path = 'data/example_with_misspelled_correction_candidates.csv'
    df.to_csv(output_path, index=False)
    print(f"\nProcessing complete! Results saved to {output_path}")


if __name__ == '__main__':
    main()
