import re
from decimal import Decimal
from toolkit.errors import NegativeDistanceError , BelowAbsoluteZeroError


patterns = {
    'length': re.compile(
        r'^(?P<value>[+-]?\d+(?:[.,]\d+)?)\s*(?P<unit>mm|cm|km|m)$',
        re.IGNORECASE
    ),
    'temp': re.compile(
        r'^(?P<value>[+-]?\d+(?:[.,]\d+)?)\s*(?P<unit>°?\s*[CFK])$',
        re.IGNORECASE
    ),
    'weight': re.compile(
        r'^(?P<value>[+-]?\d+(?:[.,]\d+)?)\s*(?P<unit>kg|g)$',
        re.IGNORECASE
    ),
}



def to_normal(number: Decimal) -> str:
    number = number.normalize()
    if number == 0:
        return "0.0"
    result = format(number, "f")
    if "." not in result:
        return result + ".0"
    result = result.rstrip("0").rstrip(".")
    return result if "." in result else result + ".0"




def type_line(line: str) -> list | None:
    line = line.strip()
    for type_, pattern in patterns.items():
        re_result = pattern.fullmatch(line)
        if re_result:
            value = Decimal(re_result.group('value').replace(',', '.'))
            unit = re_result.group('unit').replace(' ', '')
            return [type_, value, unit.lower()]
    raise ValueError('Неверное значение')


#length
def to_mm(data: list) -> list:
    values = {
        'mm': 1,
        'cm': 10,
        'm': 1000,
        'km': 1_000_000
    }
    return [data[0], data[1] * Decimal(str(values[data[2]])), 'mm']


def length_main(data: list) -> list:
    if data[1] < 0:
        raise NegativeDistanceError('Расстояние не может быть отрицательным')
    data = to_mm(data)
    factors = ['1', '0.1', '0.001', '0.000001']
    digits = [data[1] * Decimal(factors[x]) for x in range(len(factors))]
    values = ['mm', 'cm', 'm', 'km']
    return [to_normal(digits[i])+values[i] for i in range(len(values))]


#temp
def to_celsius(data: list) -> list:
    if data[2] == 'k' or data[2] == '°k':
        data[1] = data[1] - Decimal('273.15')
    if data[2] == 'f' or data[2] == '°f':
        data[1] = (data[1] - Decimal('32')) * Decimal('5') / Decimal('9')
    data[2]='c'
    return data


def temp_main(data: list) -> list:
    data = to_celsius(data)
    F = data[1] * Decimal('1.8') + Decimal('32')
    K = data[1] + Decimal('273.15')
    if K<0:
        raise BelowAbsoluteZeroError('Температура ниже абсолютного нуля')
    digits = [data[1],F,K]
    values = ['C','F','K']
    return [to_normal(digits[i])+values[i] for i in range(len(values))]


#weight
def weight_main(data: list) -> list:
    if data[2]=='kg':
        digits=[data[1] * Decimal('1000'),data[1]]
    elif data[2]=='g':
        digits=[data[1],data[1] * Decimal('0.001')]
    values = ['g','kg']
    return [to_normal(digits[i])+values[i] for i in range(len(values))]



#converter result
def convert(line: str, to_unit: str | None = None) -> str:
    line = type_line(line)
    if line[0]=='length':
        result = length_main(line)
        units = ['mm', 'cm', 'm', 'km']
    if line[0]=='temp':
        result = temp_main(line)
        units = ['c', 'f', 'k']
    if line[0]=='weight':
        result = weight_main(line)
        units = ['g', 'kg']
    if to_unit is not None:
        target = to_unit.strip().lower()
        if target not in units:
            raise ValueError('Неверное значение')
        return result[units.index(target)]
    return ' - '.join(result)