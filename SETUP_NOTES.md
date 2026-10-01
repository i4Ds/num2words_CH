# num2words_CH — setup & status notes

Getting the full `convert_numbers` pipeline (HeidelTime date/time tagging + spaCy
ordinal detection + Swiss-German verbalization) running from a fresh clone.

## Dependencies

```bash
conda create -n num2words_ch -c conda-forge python=3.11 'openjdk=11' -y
conda activate num2words_ch
pip install spacy==3.8.11 jpype1==1.6.0 py-heideltime==1.0.6 emoji==2.0.0 \
            pandas openpyxl python-dateutil click typer pytest
pip install "https://github.com/explosion/spacy-models/releases/download/de_core_news_sm-3.8.0/de_core_news_sm-3.8.0-py3-none-any.whl"
```

HeidelTime runs the bundled standalone JAR via jpype, so a JVM is required.
`JAVA_HOME` must point at a JDK **before** the first `heideltime()` call:

```bash
export JAVA_HOME="$CONDA_PREFIX/lib/jvm"   # conda openjdk
```

## Two non-obvious clone fixes

1. **TreeTagger binaries need the execute bit.** After clone the files under
   `py_heideltime/Heideltime/TreeTaggerLinux/{bin,cmd}/` are not executable and
   HeidelTime silently produces no DATE/TIME spans. Fixed in this repo (mode bits
   committed); if it regresses: `chmod +x py_heideltime/Heideltime/TreeTaggerLinux/{bin,cmd}/*`.
2. **`config.props` is runtime-generated** by `py_heideltime.config._write_config_props()`
   and contains a machine-specific `treeTaggerHome` path. It is now gitignored —
   do not commit it.

## Running the tests

```bash
JAVA_HOME="$CONDA_PREFIX/lib/jvm" python -m pytest \
  tests/test_heideltime_tagging.py \
  tests/test_ch_conversion_edgecases.py \
  tests/test_ch_bs_conversion.py -v
```

`tests/test_de.py` and `tests/test_en.py` currently fail at *collection* with
`ImportError: cannot import name 'num2words' from 'num2words'` — pre-existing; they
target the upstream `num2words` package API that this fork restructured.

## Status (what works)

`convert_numbers(text, dialect)` for
`dialect in {"ch_bs", "ch_sg", "ch_zh", "ch_lu", "ch_be"}` handles:

- plain / large numbers, de-CH thousands (`1.234`, `1'000`) and `,` decimals (`1.234,56`)
- dates (`24.12.2024`, `25.5.13`, `1. Januar 2020`, year-only) via HeidelTime
- Swiss colloquial times (`18:00`→"sechsi", `10:30`→"halb elfi", `7:45`→"viertl vor achti")
- phone numbers (digit-by-digit, `+` → "plus"), Swiss ZIP codes
- alphanumeric model codes left intact (`A380`, `CO2`, `G8`, `3D`, `A2`)
- lexical/relative temporals (`Weihnachten`, `heute`, `morgen`) left untouched —
  only digit-bearing DATE/TIME spans are verbalized

Luzern (`ch_lu`) and Bern (`ch_be`) have standalone dialect modules, with
spellings transcribed from `Luzerndeutsch_lf.xlsx` and `Bärndütsch-übersetzt.csv`.
These two source files can be deleted after setup: neither the converters nor
their tests read them. Keep the existing `numbers_helper.xlsx` and
`PLZ_Ortschaften.csv`, which the other dialects and detection pipeline still use.
Both new dialects support the same `num2words` and `convert_numbers` APIs:

```python
from num2words.num2words_CH import num2words
from num2words.detect_convert_ch_numbers import convert_numbers

num2words(132, lang="ch_lu")  # eihondertzwoiedriisg
num2words(132, lang="ch_be")  # hundertzwöiedrissg
convert_numbers("Um 14:45", "ch_lu")  # Um viertelvor drü
convert_numbers("Um 14:45", "ch_be")  # Um viertäl vor drü
```

Number words are lowercased and trimmed. Explicit compound examples retain
the reference spelling, even where it differs from the individual digits.
Ordinal endings were transcribed from the 48 translated grammar examples;
unlisted forms are generated from these patterns. Source spelling variations
(such as Bern's `zweite` alongside `zwöite`) are preserved in the references.
The existing pipeline treats midnight as hour 12 (`zwölfi`), even though the
new references also list a separate midnight word.

Run the Luzern/Bern reference and pipeline checks with:

```bash
JAVA_HOME="$CONDA_PREFIX/lib/jvm" python -m pytest tests/test_ch_lu_be_conversion.py -v
```

## Known limitations

- **Mixed dot thousands and comma decimals** (`1.234,56`) can be split by
  temporal detection before numeric conversion, leaving a comma behind.
  The existing Basel/St. Gallen edge-case tests reproduce this failure.
- **German (`lang='de'`) is not supported by `convert_numbers`** — `'de'` is
  commented out of `CONVERTER_CLASSES` (num2words_CH.py) and the type-aware
  date/time/ordinal verbalization is only implemented for the Swiss dialects.
  `convert_numbers(text, 'de')` raises `NotImplementedError`.
- **Ordinals without a determiner** are not always detected. Ordinal detection
  (`_is_ordinal_context`) only fires when the number is preceded by a determiner
  or preposition (`der 2.`, `am 3.`). Accusative objects like
  "Ich betrachte 2. Satz" are read as a plain number ("zwei.") — this is the cause
  of the 2 remaining failures in `tests/test_ch_bs_conversion.py`
  (`test_ordinal_numbers`, `test_mixed_content`).
- **Currency words** (`Fr.`, `CHF`) are not expanded to "Franken"; MONEY detection
  is disabled. The amount is verbalized but the currency token is left as-is.
