import os
import sys
import unittest


sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from num2words.num2words_CH import num2words


class TestCHZHConversion(unittest.TestCase):
    def test_cardinals_follow_zurich_helper_examples(self):
        expected = {
            0: "null",
            5: "foif",
            6: "sachs",
            42: "zweievierzg",
            85: "foifedachzg",
            100: "hundert",
            132: "hunderzweiedriisg",
            1000: "tuusig",
            6343: "sachstuusigdrühundertdrüevierzg",
        }
        for value, spoken in expected.items():
            with self.subTest(value=value):
                self.assertEqual(num2words(value, lang="ch_zh"), spoken)

    def test_decimal_ordinal_date_and_time_helpers(self):
        self.assertEqual(num2words("3,5", lang="ch_zh"), "drü Komma foif")
        self.assertEqual(
            num2words(
                3,
                lang="ch_zh",
                ordinal=True,
                declension={
                    "declension": "schwach",
                    "gender": "masc",
                    "case": "nom",
                },
            ),
            "dritti",
        )
        self.assertEqual(num2words(9, lang="ch_zh", to="month_dates"), "Septamber")
        self.assertEqual(num2words(10, lang="ch_zh", to="hours"), "zani")
        self.assertEqual(num2words(45, lang="ch_zh", to="minutes"), "viertel vor")
        self.assertEqual(num2words("sek", lang="ch_zh", to="lookup"), "Sekunde")


if __name__ == "__main__":
    unittest.main()
