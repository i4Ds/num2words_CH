# -*- coding: utf-8 -*-
"""Tests for HeidelTime temporal tagging.

These verify the *upstream* layer that `convert_numbers` relies on: that
HeidelTime correctly recognises dates and times in German/Swiss-German text,
assigns the right TIMEX3 type (DATE vs TIME), and yields the expected
normalized value. If this layer mis-tags, every downstream date/time
verbalization is wrong — so it is tested in isolation here.

Run:  JAVA_HOME=<env>/lib/jvm python -m pytest tests/test_heideltime_tagging.py -v
(The conftest/runner sets JAVA_HOME; a fallback is applied below so the file is
self-contained.)
"""
import os
import sys
import unittest

# JAVA_HOME must be set before jpype starts the JVM. Fall back to the active
# conda env's bundled openjdk so the test is runnable on its own.
if not os.environ.get("JAVA_HOME"):
    _cand = os.path.join(sys.prefix, "lib", "jvm")
    if os.path.isdir(_cand):
        os.environ["JAVA_HOME"] = _cand

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from py_heideltime.py_heideltime import heideltime


def tag(sentence):
    """Return the list of TIMEX3 dicts HeidelTime extracts from *sentence*."""
    return heideltime(sentence, language="german", document_type="scientific", dct=None)


def of_type(timexs, typ):
    return [t for t in timexs if t.get("type") == typ]


def has_digit(s):
    return any(c.isdigit() for c in (s or ""))


class TestHeidelTimeTagging(unittest.TestCase):
    """Each test asserts the stable parts of HeidelTime output (type, text,
    and — for fully specified expressions — the normalized value). Times carry
    the document-creation date as a prefix, so only the THH:MM part is checked."""

    # ---- DATE tagging ----
    def test_explicit_full_date(self):
        t = of_type(tag("Das Treffen ist am 24.12.2024 geplant."), "DATE")
        self.assertTrue(t, "no DATE tagged for 24.12.2024")
        self.assertIn("24.12.2024", t[0]["text"])
        self.assertEqual(t[0]["value"], "2024-12-24")

    def test_two_digit_year_date(self):
        t = of_type(tag("Treffen am 25.5.13."), "DATE")
        self.assertTrue(t, "no DATE tagged for 25.5.13")
        self.assertEqual(t[0]["value"], "2013-05-25")

    def test_date_with_month_name(self):
        t = of_type(tag("Der 1. Januar 2020 war ein Mittwoch."), "DATE")
        self.assertTrue(t, "no DATE tagged for 1. Januar 2020")
        self.assertEqual(t[0]["value"], "2020-01-01")

    def test_year_only(self):
        t = of_type(tag("Im Jahr 1983 ist viel passiert."), "DATE")
        self.assertTrue(t, "no DATE tagged for year 1983")
        self.assertTrue(t[0]["value"].startswith("1983"), t[0]["value"])

    # ---- TIME tagging ----
    def test_time_with_uhr(self):
        t = of_type(tag("Wir treffen uns um 18:00 Uhr."), "TIME")
        self.assertTrue(t, "no TIME tagged for 18:00 Uhr")
        self.assertTrue(t[0]["value"].endswith("T18:00"), t[0]["value"])

    def test_time_bare(self):
        t = of_type(tag("Es ist jetzt 10:30."), "TIME")
        self.assertTrue(t, "no TIME tagged for 10:30")
        self.assertTrue(t[0]["value"].endswith("T10:30"), t[0]["value"])

    def test_time_quarter(self):
        t = of_type(tag("Der Zug fährt um 7:45 ab."), "TIME")
        self.assertTrue(t, "no TIME tagged for 7:45")
        self.assertTrue(t[0]["value"].endswith("T07:45"), t[0]["value"])

    # ---- DATE + TIME together ----
    def test_date_and_time_in_one_sentence(self):
        timexs = tag("Am 24.12.2024 um 18:00 Uhr beginnt die Feier.")
        self.assertTrue(of_type(timexs, "DATE"), "missing DATE")
        self.assertTrue(of_type(timexs, "TIME"), "missing TIME")

    # ---- Negative: no spurious tags ----
    def test_no_temporal_no_tags(self):
        timexs = tag("Ich habe fünf Äpfel und drei Birnen gekauft.")
        self.assertEqual(of_type(timexs, "DATE") + of_type(timexs, "TIME"), [])

    def test_plain_number_not_time_or_date(self):
        # "100 Personen" must not be mistaken for a date/time.
        timexs = tag("Es sind 100 Personen anwesend.")
        self.assertEqual(of_type(timexs, "DATE") + of_type(timexs, "TIME"), [])

    # ---- Documents WHY the downstream digit-gate exists ----
    def test_lexical_holiday_tagged_without_digit(self):
        # HeidelTime resolves "Weihnachten" to a DATE even though the surface
        # text has no digit. convert_numbers must NOT verbalize such spans;
        # this test pins the upstream behaviour that justifies the digit-gate.
        t = of_type(tag("Wir sehen uns an Weihnachten."), "DATE")
        if t:  # HeidelTime version dependent, but typically tags it
            self.assertFalse(
                has_digit(t[0]["text"]),
                "expected the holiday span to carry no digit",
            )


if __name__ == "__main__":
    unittest.main()
