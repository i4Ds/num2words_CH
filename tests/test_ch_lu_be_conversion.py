"""Reference data and full-text regression checks for Luzern and Bern."""

import os
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
os.environ.setdefault("JAVA_HOME", str(Path(sys.prefix) / "lib" / "jvm"))

from num2words.num2words_CH import num2words


@pytest.mark.parametrize("dialect,expected", [('ch_lu',
  {0: 'noll',
   1: 'eis',
   2: 'zwoi',
   3: 'drü',
   4: 'vier',
   5: 'füüf',
   6: 'sächs',
   7: 'sebe',
   8: 'acht',
   9: 'nüün',
   10: 'zäh',
   11: 'elf',
   12: 'zwölf',
   13: 'drizäh',
   14: 'vierzäh',
   15: 'föfzäh',
   16: 'sächzäh',
   17: 'sebzäh',
   18: 'achtzäh',
   19: 'nüünzäh',
   20: 'zwänzg',
   30: 'driisg',
   40: 'vierzg',
   50: 'föfzg',
   60: 'sächzg',
   70: 'sebezg',
   80: 'achtzg',
   85: 'füüfedachzg',
   90: 'nünzg',
   100: 'eihondert',
   132: 'eihondertzwoiedriisg',
   200: 'zwoihondert',
   1000: 'tuusig',
   6343: 'sächstuusigdrühondertdrüevierzg',
   10000: 'zähtuusig'}),
 ('ch_be',
  {0: 'null',
   1: 'eis',
   2: 'zwöi',
   3: 'drü',
   4: 'vier',
   5: 'füüf',
   6: 'sächs',
   7: 'siebe',
   8: 'acht',
   9: 'nüün',
   10: 'zäh',
   11: 'elf',
   12: 'zwölf',
   13: 'drizäh',
   14: 'vierzäh',
   15: 'föfzäh',
   16: 'sächzäh',
   17: 'siebezäh',
   18: 'achzäh',
   19: 'nünzäh',
   20: 'zwänzg',
   30: 'drissg',
   40: 'vierzg',
   50: 'füfzg',
   60: 'sächzg',
   70: 'siebäzg',
   80: 'achtzg',
   85: 'füfeachzg',
   90: 'nünzg',
   100: 'hundert',
   132: 'hundertzwöiedrissg',
   200: 'zwöihundert',
   1000: 'tuusig',
   6343: 'sächstuusigdrühundertdrüevierzg',
   10000: 'zähtuusig'})])
def test_all_explicit_cardinal_examples(dialect, expected):
    for value, spoken in expected.items():
        assert num2words(value, lang=dialect) == spoken


@pytest.mark.parametrize("dialect,two,fortytwo,third,first,month,hour,quarter,half,seconds", [
    ("ch_lu", "zwoi", "zwoievierzg", "drett", "erst", "Märze", "sebni", "viertelvor", "halbi", "Sekonde"),
    ("ch_be", "zwöi", "zwöievierzg", "dritt", "erscht", "März", "sibni", "viertäl vor", "halb", "Sekundä"),
])
def test_generated_numbers_and_helpers(dialect, two, fortytwo, third, first, month, hour, quarter, half, seconds):
    assert num2words(42, lang=dialect) == fortytwo
    assert num2words(-42, lang=dialect) == "minus " + fortytwo
    assert num2words("2,5", lang=dialect) == two + " Komma füüf"
    declension = {"declension": "schwach", "gender": "masc", "case": "nom"}
    assert num2words(3, lang=dialect, ordinal=True, declension=declension) == third
    declension["case"] = "dat"
    assert num2words(1, lang=dialect, ordinal=True, declension=declension) == first + "e"
    assert num2words(23, lang=dialect, ordinal=True, declension=declension) == num2words(23, lang=dialect) + "schte"
    assert num2words(3, lang=dialect, to="month_dates") == month
    assert num2words(7, lang=dialect, to="hours") == hour
    assert num2words(45, lang=dialect, to="minutes") == quarter
    assert num2words(30, lang=dialect, to="minutes") == half
    assert num2words("sek", lang=dialect, to="lookup") == seconds
    assert num2words(1999, lang=dialect, to="year").startswith(num2words(19, lang=dialect) + ("hondert" if dialect == "ch_lu" else "hundert"))


@pytest.mark.parametrize("dialect,two,quarter,half,first,month", [
    ("ch_lu", "zwoi", "viertelvor", "halbi", "erste", "Märze"),
    ("ch_be", "zwöi", "viertäl vor", "halb", "erschte", "März"),
])
def test_full_text_pipeline(dialect, two, quarter, half, first, month):
    from num2words.detect_convert_ch_numbers import convert_numbers

    assert convert_numbers("Es sind 42 Stück", dialect) == "Es sind " + two + "evierzg Stück"
    assert convert_numbers("Um 14:45", dialect) == "Um " + quarter + " drü"
    assert convert_numbers("Um 14:30", dialect) == "Um " + half + " drü"
    assert convert_numbers("Am 1.3.2024", dialect) == "Am " + first + " " + month + " " + num2words(2024, lang=dialect)
    assert "plus vier eis" in convert_numbers("Tel: +41 79 123 45 67", dialect)
    assert convert_numbers("A380 und CO2", dialect) == "A380 und CO2"
    assert convert_numbers("Es kostet 2,5 Franken", dialect) == "Es kostet " + two + " Komma füüf Franken"
    assert convert_numbers("Es git 1'000 Lüt", dialect) == "Es git tuusig Lüt"
