import pytest

from decimal import Decimal

from toolkit.converter import convert, type_line
from toolkit.errors import NegativeDistanceError, BelowAbsoluteZeroError


def test_length():
    assert convert("1mm", "cm") == "0.1cm"
    assert convert("1cm", "mm") == "10.0mm"
    assert convert("1m", "cm") == "100.0cm"
    assert convert("1km", "m") == "1000.0m"


def test_length_comma():
    assert convert("2,5m", "cm") == "250.0cm"


def test_length_space():
    assert convert("  2 KM  ", "m") == "2000.0m"
    assert convert(" 15 CM ", "m") == "0.15m"


def test_temp_celsius():
    assert convert("0C", "F") == "32.0F"
    assert convert("100C", "K") == "373.15K"
    assert convert("-273.15C", "K") == "0.0K"


def test_temp_farengheit():
    assert convert("32F", "C") == "0.0C"
    assert convert("212F", "C") == "100.0C"


def test_temp_kelvin():
    assert convert("273.15K", "C") == "0.0C"
    assert convert("373.15K", "F") == "212.0F"


def test_temp_space():
    assert convert("0 C", "F") == "32.0F"
    assert convert("32  F", "K") == "273.15K"
    assert convert("273.15 K", "C") == "0.0C"


def test_weight():
    assert convert("1g", "kg") == "0.001kg"
    assert convert("1000g", "kg") == "1.0kg"
    assert convert("1kg", "g") == "1000.0g"
    assert convert("2.5kg", "g") == "2500.0g"


def test_weight_space_comma():
    assert convert("2,5 kg", "g") == "2500.0g"
    assert convert(" 500 G ", "kg") == "0.5kg"


def test_type_line():
    assert type_line("12cm") == ["length", Decimal("12"), "cm"]
    assert type_line("25,5 kg") == ["weight", Decimal("25.5"), "kg"]
    assert type_line("32F") == ["temp", Decimal("32"), "f"]
    assert type_line(" 0 C ") == ["temp", Decimal("0"), "c"]


def test_negative_length():
    with pytest.raises(NegativeDistanceError):
        convert("-1mm", "cm")

    with pytest.raises(NegativeDistanceError):
        convert("-2.5m", "cm")

    with pytest.raises(NegativeDistanceError):
        convert("-1km", "m")


def test_temp_below_zero():
    with pytest.raises(BelowAbsoluteZeroError):
        convert("-274C", "K")

    with pytest.raises(BelowAbsoluteZeroError):
        convert("-500F", "C")

    with pytest.raises(BelowAbsoluteZeroError):
        convert("-1K", "C")


def test_wrong_input():
    with pytest.raises(ValueError):
        convert("hello", "m")

    with pytest.raises(ValueError):
        convert("10", "m")

    with pytest.raises(ValueError):
        convert("5l", "m")

    with pytest.raises(ValueError):
        convert("12 meters", "cm")

    with pytest.raises(ValueError):
        convert("kg", "g")

    with pytest.raises(ValueError):
        convert("10CC", "F")

    with pytest.raises(ValueError):
        convert("10m", "kg")