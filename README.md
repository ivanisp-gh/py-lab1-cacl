# py-lab1-calc

## Описание

Программа представляет собой калькулятор и конвертер величин, работающие через командную строку.

Калькулятор вычисляет математические выражения, а конвертер переводит единицы длины, массы и температуры.

## Структура программы

```text
src/
└── toolkit/
    ├── __main__.py
    ├── calculator.py
    ├── converter.py
    └── errors.py

tests/
├── test_calculator.py
└── test_converter.py
```

В папке `src/toolkit/` находится основной код программы, а в папке `tests/` — тесты.

## Установка

Для работы программы необходим Python 3.10 или новее. Для запуска тестов нужна библиотека `pytest`:

```powershell
python -m pip install pytest
```

## Запуск программы

Откройте PowerShell в папке проекта:

```powershell
cd "...\py-lab1-calc"
$env:PYTHONPATH = "$PWD\src"
```

После этого можно запускать программу командой `python -m toolkit`.

## Калькулятор

Для вычисления выражений используется команда `calc`:

```powershell
python -m toolkit calc "2+2*2"
python -m toolkit calc "(2+2)*2"
python -m toolkit calc "10/2"
python -m toolkit calc "7%2"
python -m toolkit calc "7//3"
```

Поддерживаемые операции:

| Операция | Описание |
|---|---|
| `+` | Сложение |
| `-` | Вычитание |
| `*` | Умножение |
| `/` | Деление |
| `//` | Деление с округлением вниз |
| `%` | Остаток от деления |
| `()` | Скобки |

## Конвертер величин

Для перевода величин используется команда `convert`.

### Перевод во все доступные единицы

**Длина** (`mm`, `cm`, `m`, `km`):

```powershell
python -m toolkit convert 10cm
python -m toolkit convert 2m
python -m toolkit convert 3km
```

Например, `python -m toolkit convert 10cm` выводит:

```text
100.0mm - 10.0cm - 0.1m - 0.0001km
```

**Масса** (`g`, `kg`):

```powershell
python -m toolkit convert 500g
python -m toolkit convert 2kg
```

**Температура** (`C`, `F`, `K`):

```powershell
python -m toolkit convert 25C
python -m toolkit convert 32F
python -m toolkit convert 273.15K
```

### Перевод в конкретную единицу

Для этого используются аргументы `--from` и `--to`:

```powershell
python -m toolkit convert 80 --from mm --to cm
python -m toolkit convert 2 --from km --to m
python -m toolkit convert 500 --from g --to kg
python -m toolkit convert 100 --from C --to F
```

Например, первая команда выводит:

```text
8.0cm
```

### Особенности ввода

Можно использовать точку или запятую в дробных числах:

```powershell
python -m toolkit convert 2.5kg
python -m toolkit convert "2,5 kg"
```

Если между числом и единицей измерения есть пробел, аргумент нужно заключить в кавычки. Регистр букв в обозначениях единиц не имеет значения.

Конвертер сообщает об ошибке при некорректном формате, неизвестных или несовместимых единицах, отрицательном расстоянии и температуре ниже абсолютного нуля.

## Тесты

Запустить все тесты:

```powershell
python -m pytest -v
```

Только тесты калькулятора:

```powershell
python -m pytest tests/test_calculator.py -v
```

Только тесты конвертера:

```powershell
python -m pytest tests/test_converter.py -v
```

## Справка

```powershell
python -m toolkit --help
```
