# Khakas Spell Checker

A spell checking tool for the Khakas language, built using Python and the `pyspellchecker` library. This project includes tools for building and validating Khakas language dictionaries.

## Features

- Build custom Khakas language dictionaries from text corpora
- Validate and clean Khakas words based on language-specific rules
- Generate frequency-based word lists for spell checking
- Support for Khakas-specific characters and diacritics

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/khakas_spell_checker.git
   cd khakas_spell_checker
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Building a Dictionary

1. Prepare your Khakas text corpus (plain text file with `.txt` extension)
2. Run the dictionary builder:
   ```bash
   python build_dict.py --input path/to/your/corpus.txt --output data/khakas_dictionary.json
   ```

### Using the Spell Checker

```python
from spellchecker import SpellChecker

# Load the Khakas dictionary
spell = SpellChecker(language=None)
spell.word_frequency.load_dictionary('data/khakas_dictionary.json')

# Check spelling
word = "хакасча"
if word not in spell:
    print(f"Possible corrections: {spell.candidates(word)}")
```

## Project Structure

- `build_dict.py`: Script for building and validating Khakas dictionaries
- `spell_checker.py`: Example implementation of the spell checker
- `data/`: Directory for storing dictionary files
- `requirements.txt`: Project dependencies

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

# Проверка орфографии на хакасском языке

Инструмент для проверки орфографии на хакасском языке, созданный с использованием Python и библиотеки `pyspellchecker`. Проект включает инструменты для создания и проверки словарей хакасского языка.

## Возможности

- Создание пользовательских словарей хакасского языка из текстовых корпусов
- Проверка и очистка слов хакасского языка на основе языковых правил
- Генерация частотных списков слов для проверки орфографии
- Поддержка специфических символов и диакритики хакасского языка

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/yourusername/khakas_spell_checker.git
   cd khakas_spell_checker
   ```

2. Создайте и активируйте виртуальное окружение (рекомендуется):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # В Windows: .venv\Scripts\activate
   ```

3. Установите необходимые зависимости:
   ```bash
   pip install -r requirements.txt
   ```

## Использование

### Создание словаря

1. Подготовьте корпус текстов на хакасском языке (текстовый файл с расширением `.txt`)
2. Запустите скрипт для создания словаря:
   ```bash
   python build_dict.py --input путь/к/вашему/корпусу.txt --output data/khakas_dictionary.json
   ```

### Использование проверки орфографии

```python
from spellchecker import SpellChecker

# Загрузка словаря хакасского языка
spell = SpellChecker(language=None)
spell.word_frequency.load_dictionary('data/khakas_dictionary.json')

# Проверка орфографии
word = "хакасча"
if word not in spell:
    print(f"Возможные исправления: {spell.candidates(word)}")
```

## Структура проекта

- `build_dict.py`: Скрипт для создания и проверки словарей
- `spell_checker.py`: Пример реализации проверки орфографии
- `data/`: Директория для хранения файлов словарей
- `requirements.txt`: Зависимости проекта

## Лицензия

Этот проект распространяется под лицензией MIT - подробности см. в файле [LICENSE](LICENSE).
