# -*- coding: utf-8 -*-
"""Edge-case regression tests for convert_numbers (ch_bs + ch_sg + ch_zh).

These lock in the reliability fixes:
  * DATE over-eagerness: HeidelTime tags holidays / relative words
    ("Weihnachten", "heute") as dates; those must NOT be verbalized
    (only spans containing a digit are converted).
  * de-CH thousands/decimal: "1.234,56" / "1'000" read correctly.
  * Alphanumeric model codes (A380, CO2, G8, 3D, A2) must stay intact.
  * Phone numbers have no stray double space.
  * Times use the Swiss colloquial forms.

Run:  JAVA_HOME=<env>/lib/jvm python -m pytest tests/test_ch_conversion_edgecases.py -v
"""
import os
import sys
import unittest

if not os.environ.get("JAVA_HOME"):
    _cand = os.path.join(sys.prefix, "lib", "jvm")
    if os.path.isdir(_cand):
        os.environ["JAVA_HOME"] = _cand

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from num2words.detect_convert_ch_numbers import convert_numbers


class _Base:
    dialect = None

    def c(self, text):
        return convert_numbers(text, self.dialect)

    # ---- DATE over-eagerness ----
    def test_holiday_not_verbalized(self):
        out = self.c("Am 24.12.2024 ist Weihnachten.")
        self.assertIn("Weihnachten", out)          # word preserved
        self.assertNotIn("zweitusigsechs", out)    # not turned into today+xmas
        self.assertNotIn("zweituusigsechs", out)

    def test_relative_words_untouched(self):
        self.assertEqual(self.c("Heute ist ein schöner Tag."),
                         "Heute ist ein schöner Tag.")
        self.assertEqual(self.c("Morgen treffen wir uns."),
                         "Morgen treffen wir uns.")

    # ---- thousands / decimals (de-CH: '.' or "'" thousands, ',' decimal) ----
    def test_thousands_dot_and_decimal(self):
        out = self.c("Es kostet 1.234,56 Franke")  # no trailing '.' to keep the check simple
        self.assertIn("Komma", out)                # decimal read as "Komma <digits>"
        self.assertNotIn(",", out)                 # no leftover decimal comma
        self.assertNotIn(".", out)                 # no leftover thousands dot
        self.assertNotIn("1", out)                 # the digits are fully verbalized

    def test_apostrophe_thousands(self):
        out = self.c("Es git 1'000 Lüt.")
        self.assertIn("tusig", out.replace("tuusig", "tusig"))
        self.assertNotIn("'", out)

    def test_decimal_simple(self):
        self.assertIn("Komma", self.c("Das sind 3,5 Kilogramm."))

    # ---- alphanumeric model codes stay intact ----
    def test_model_codes_preserved(self):
        for code in ["A380", "CO2", "A2", "3D-Effekt", "G8-Länder"]:
            out = self.c(f"Das ist {code} hier.")
            self.assertIn(code, out, f"{code} should be left intact, got: {out}")

    def test_real_number_still_converted_after_word(self):
        # "Boeing 747" — space-separated => a real number, must convert.
        out = self.c("Die Boeing 747 fliegt.")
        self.assertNotIn("747", out)

    # ---- phone: no double space ----
    def test_phone_no_double_space(self):
        out = self.c("Ruf 044 123 45 67 an.")
        self.assertNotIn("  ", out)
        self.assertIn("null", out)

    # ---- plain numbers / large numbers regression ----
    def test_plain_and_large(self):
        out = self.c("Es sind 1000000 Lüt.").lower()
        self.assertIn("million", out)              # 1'000'000 -> "...million..."
        self.assertNotIn("1000000", out)


class TestEdgeCasesCHBS(_Base, unittest.TestCase):
    dialect = "ch_bs"

    def test_times_swiss(self):
        self.assertIn("sechsi", self.c("Um 18:00 Uhr."))
        self.assertIn("fünf ab zwölfi", self.c("Um 0:05."))
        self.assertIn("halb elfi", self.c("Treffpunkt 10:30."))
        self.assertIn("viertl vor achti", self.c("Es ist 7:45."))


class TestEdgeCasesCHSG(_Base, unittest.TestCase):
    dialect = "ch_sg"

    def test_times_swiss(self):
        self.assertIn("sechsi", self.c("Um 18:00 Uhr."))
        self.assertIn("füfab zwölfi", self.c("Um 0:05."))
        self.assertIn("halbi elfi", self.c("Treffpunkt 10:30."))
        self.assertIn("viertl vor achti", self.c("Es ist 7:45."))


class TestEdgeCasesCHZH(unittest.TestCase):
    def c(self, text):
        return convert_numbers(text, "ch_zh")

    def test_plain_number(self):
        self.assertEqual(self.c("Ich habe 5 Äpfel."), "Ich habe foif Äpfel.")

    def test_times_swiss(self):
        self.assertIn("sachsi", self.c("Um 18:00 Uhr."))
        self.assertIn("foif ab zwölfi", self.c("Um 0:05."))
        self.assertIn("halbi elfi", self.c("Treffpunkt 10:30."))
        self.assertIn("viertel vor achti", self.c("Es ist 7:45."))


if __name__ == "__main__":
    unittest.main()
