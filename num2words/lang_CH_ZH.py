# -*- coding: utf-8 -*-
"""Zürich German number-to-words converter."""

from __future__ import print_function, unicode_literals

import os
import re

import pandas as pd

from .lang_EU import Num2Word_EU


_HELPER_DATA = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "helper_data"
)
_HELPER_FILE = os.path.join(_HELPER_DATA, "numbers_helper.xlsx")


def _clean(value, fallback=None):
    if pd.isna(value):
        return fallback
    return str(value).strip()


class Num2Word_CH_ZH(Num2Word_EU):
    """Render numbers using the Zürich columns in ``numbers_helper.xlsx``."""

    CURRENCY_FORMS = {
        "EUR": (("Euro", "Euro"), ("Cent", "Cent")),
        "GBP": (("Pfund", "Pfund"), ("Penny", "Pence")),
        "USD": (("Dollar", "Dollar"), ("Cent", "Cent")),
        "CNY": (("Yuan", "Yuan"), ("Jiao", "Fen")),
        "DEM": (("Mark", "Mark"), ("Pfennig", "Pfennig")),
    }

    GIGA_SUFFIX = "illiarde"
    MEGA_SUFFIX = "illion"

    def setup(self):
        numbers = pd.read_excel(_HELPER_FILE, sheet_name="Numbers")
        number_values = {}
        for _, row in numbers.iterrows():
            key = row["Nummerisch/ Beispiel"]
            if isinstance(key, (int, float)) and not pd.isna(key):
                number_values[int(key)] = _clean(row["Zürich"])

        self.ordinal_declension = pd.read_excel(
            _HELPER_FILE, sheet_name="Ordinal_deklination"
        )[["Deklination", "Genus", "Kasus", "Zürich_short"]]
        self.ordinal_declension["Zürich_short"] = self.ordinal_declension[
            "Zürich_short"
        ].fillna("")
        self.ordinal_declension["Kasus"] = self.ordinal_declension["Kasus"].str.lower()

        self.negword = "minus "
        self.posword = "plus "
        self.pointword = _clean(
            numbers.loc[numbers["Nummerisch/ Beispiel"] == ",", "Zürich"].iloc[-1],
            "Komma",
        )
        self.errmsg_floatord = "Die Gleitkommazahl %s kann nicht in eine Ordnungszahl konvertiert werden."
        self.errmsg_nonnum = "Nur Zahlen (type(%s)) können in Wörter konvertiert werden."
        self.errmsg_negord = "Die negative Zahl %s kann nicht in eine Ordnungszahl konvertiert werden."
        self.errmsg_toobig = "Die Zahl %s muss kleiner als %s sein."
        self.exclude_title = []

        lows = ["Non", "Okt", "Sept", "Sext", "Quint", "Quadr", "Tr", "B", "M"]
        units = ["", "un", "duo", "tre", "quattuor", "quin", "sex", "sept", "okto", "novem"]
        tens = [
            "dez", "vigint", "trigint", "quadragint", "quinquagint",
            "sexagint", "septuagint", "oktogint", "nonagint",
        ]
        self.high_numwords = ["zent"] + self.gen_high_numwords(units, tens, lows)
        self.mid_numwords = [
            (1000, number_values[1000]),
            (100, number_values[100]),
            *[(value, number_values[value]) for value in range(90, 20, -10)],
        ]
        self.low_numwords = [
            number_values[value] if value else (number_values.get(0) or "null")
            for value in range(20, -1, -1)
        ]
        self.ords = {
            "eis": "ers",
            "drü": "drit",
            "acht": "ach",
            "siebe": "sib",
            "zg": "zgs",
            "ert": "erts",
            "end": "ends",
            "ion": "ions",
            "nen": "ns",
            "rde": "rds",
            "rden": "rds",
            "zah": "zahn",
            "ard": "ards",
            "arde": "ards",
        }

        date_time = pd.read_excel(_HELPER_FILE, sheet_name="Zeiten & Datum")
        zh_values = {
            str(row["Nummerisch/ Beispiel"]).strip(): _clean(row["Zürich"])
            for _, row in date_time.iterrows()
            if not pd.isna(row["Zürich"])
        }
        self.minutes = {
            15: zh_values["14:15:00"].rsplit(" ", 1)[0],
            25: "foif vor halb",
            30: zh_values["14:30:00"].rsplit(" ", 1)[0],
            35: "foif ab halb",
            45: zh_values["14:45"].rsplit(" ", 1)[0],
        }
        self.hours = {
            hour: zh_values[f"{hour:02d}:00:00"] for hour in range(1, 13)
        }
        self.month_dates = {
            month: zh_values[name]
            for month, name in enumerate(
                [
                    "Januar", "Februar", "März", "April", "Mai", "Juni",
                    "Juli", "August", "September", "Oktober", "November", "Dezember",
                ],
                start=1,
            )
        }
        self.second_word = zh_values.get("Sekunden", "Sekunde")

    def merge(self, curr, next):
        ctext, cnum, ntext, nnum = curr + next

        if cnum == 1:
            if nnum in {100, 1000}:
                return (ntext, nnum)
            if nnum < 10 ** 6:
                return next
            ctext = "ei"

        if nnum > cnum:
            if nnum >= 10 ** 6:
                if cnum > 1 and ntext.endswith("e"):
                    ntext += "n"
                ctext += " "
            val = cnum * nnum
        else:
            if nnum < 10 < cnum < 100:
                if nnum == 1:
                    ntext = "ein"
                connector = "ed" if ctext.startswith("ach") else "e"
                ntext, ctext = ctext, ntext + connector
            elif cnum == 100 and nnum < 100:
                ctext = ctext.removesuffix("t")
            elif cnum >= 10 ** 6:
                ctext += " "
            val = cnum + nnum

        return ctext + ntext, val

    def to_ordinal(self, value, declension):
        self.verify_ordinal(value)
        outword = self.to_cardinal(value).lower()
        for key, replacement in self.ords.items():
            if outword.endswith(key):
                outword = outword[: -len(key)] + replacement
                break
        mask = (
            (self.ordinal_declension["Deklination"] == declension["declension"])
            & (self.ordinal_declension["Genus"] == declension["gender"])
            & (self.ordinal_declension["Kasus"] == declension["case"])
        )
        suffixes = self.ordinal_declension.loc[mask, "Zürich_short"].values
        if not len(suffixes):
            raise ValueError("Unknown Zürich German ordinal declension")
        result = outword + "t" + suffixes[0]
        if result in {"eituusigssti", "eihundertsti"}:
            result = result.replace("ei", "", 1)
        result = re.sub(r"ei ([a-z]+(illion|illiard)sti)$", lambda match: match.group(1), result)
        return re.sub(r" ([a-z]+(illion|illiard)sti)$", lambda match: match.group(1), result)

    def to_ordinal_num(self, value):
        self.verify_ordinal(value)
        return str(value) + "."

    def to_currency(self, val, currency="EUR", cents=True, separator=" und", adjective=False):
        result = super().to_currency(
            val, currency=currency, cents=cents, separator=separator, adjective=adjective
        )
        return result.replace("eis ", "ei ")

    def to_minutes(self, val):
        if val in self.minutes:
            return self.minutes[val]
        if val < 30:
            return self.to_cardinal(val) + " ab"
        if 30 < val < 60:
            return self.to_cardinal(60 - val) + " vor"

    def to_hours(self, val):
        return self.hours.get(val)

    def to_month_dates(self, val):
        return self.month_dates.get(val)

    def to_lookup(self, val):
        if val == "sek":
            return self.second_word

    def to_year(self, val, longval=True):
        if not (val // 100) % 10:
            return self.to_cardinal(val)
        return self.to_splitnum(val, hightxt="hundert", longval=longval).replace(" ", "")
