"""Bern German number-to-words converter."""

from .lang_EU import Num2Word_EU


class Num2Word_CH_BE(Num2Word_EU):
    CURRENCY_FORMS = {
        'CNY': (('Yuan', 'Yuan'), ('Jiao', 'Fen')),
        'DEM': (('Mark', 'Mark'), ('Pfennig', 'Pfennig')),
        'EUR': (('Euro', 'Euro'), ('Cent', 'Cent')),
        'GBP': (('Pfund', 'Pfund'), ('Penny', 'Pence')),
        'USD': (('Dollar', 'Dollar'), ('Cent', 'Cent')),
    }

    GIGA_SUFFIX = "illiarde"
    MEGA_SUFFIX = "illion"

    def setup(self):
        # Spellings transcribed from the supplied dialect translations.
        # The source Excel/CSV file is not needed at runtime.
        self.negword = 'minus '
        self.posword = 'plus '
        self.pointword = 'Komma'
        self.errmsg_floatord = 'Die Gleitkommazahl %s kann nicht in eine Ordnungszahl konvertiert werden.'
        self.errmsg_nonnum = 'Nur Zahlen (type(%s)) können in Wörter konvertiert werden.'
        self.errmsg_negord = 'Die negative Zahl %s kann nicht in eine Ordnungszahl konvertiert werden.'
        self.errmsg_toobig = 'Die Zahl %s muss kleiner als %s sein.'
        self.exclude_title = []
        self.mid_numwords = [
            (1000, 'tuusig'), (100, 'hundert'), (90, 'nünzg'), (80, 'achtzg'),
            (70, 'siebäzg'), (60, 'sächzg'), (50, 'füfzg'), (40, 'vierzg'),
            (30, 'drissg'),
        ]
        self.low_numwords = [
            'zwänzg', 'nünzäh', 'achzäh', 'siebezäh', 'sächzäh', 'föfzäh', 'vierzäh',
            'drizäh', 'zwölf', 'elf', 'zäh', 'nüün', 'acht', 'siebe', 'sächs', 'füüf',
            'vier', 'drü', 'zwöi', 'eis', 'null',
        ]
        self.hundred_prefix = ''
        self.number_examples = {
            0: 'null',
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
            10000: 'zähtuusig',
        }
        self.minutes = {
            15: 'viertäl ab',
            25: 'füüf vor halb',
            30: 'halb',
            35: 'füüf ab halb',
            45: 'viertäl vor',
        }
        self.hours = {
            1: 'eis',
            2: 'zwöi',
            3: 'drü',
            4: 'vieri',
            5: 'füüfi',
            6: 'sächsi',
            7: 'sibni',
            8: 'achti',
            9: 'nüüni',
            10: 'zähni',
            11: 'elfi',
            12: 'zwölfi',
        }
        self.month_dates = {
            1: 'Januar',
            2: 'Februar',
            3: 'März',
            4: 'April',
            5: 'Mei',
            6: 'Juni',
            7: 'Juli',
            8: 'Auguscht',
            9: 'Septämber',
            10: 'Oktober',
            11: 'Novämber',
            12: 'Dezämber',
        }
        self.second_word = 'Sekundä'
        self.ordinal_roots = {
            1: 'erscht',
            2: 'zwöit',
            3: 'dritt',
            7: 'sibt',
            8: 'acht',
            100: 'hundertscht',
            1000: 'tuusigscht',
            1000000: 'millionscht',
        }
        self.ordinal_endings = {
            ('gemischt', 'fem', 'acc'): 'i',
            ('gemischt', 'fem', 'dat'): 'e',
            ('gemischt', 'fem', 'gen'): 'e',
            ('gemischt', 'fem', 'nom'): 'i',
            ('gemischt', 'masc', 'acc'): 'e',
            ('gemischt', 'masc', 'dat'): 'e',
            ('gemischt', 'masc', 'gen'): 'e',
            ('gemischt', 'masc', 'nom'): 'e',
            ('gemischt', 'neut', 'acc'): 's',
            ('gemischt', 'neut', 'dat'): 'e',
            ('gemischt', 'neut', 'gen'): 'e',
            ('gemischt', 'neut', 'nom'): 's',
            ('gemischt', 'plur', 'acc'): 'e',
            ('gemischt', 'plur', 'dat'): 'e',
            ('gemischt', 'plur', 'gen'): 'e',
            ('gemischt', 'plur', 'nom'): 'e',
            ('schwach', 'fem', 'acc'): 'i',
            ('schwach', 'fem', 'dat'): 'e',
            ('schwach', 'fem', 'gen'): 'e',
            ('schwach', 'fem', 'nom'): '',
            ('schwach', 'masc', 'acc'): '',
            ('schwach', 'masc', 'dat'): 'e',
            ('schwach', 'masc', 'gen'): 'e',
            ('schwach', 'masc', 'nom'): '',
            ('schwach', 'neut', 'acc'): 'e',
            ('schwach', 'neut', 'dat'): 'e',
            ('schwach', 'neut', 'gen'): 'e',
            ('schwach', 'neut', 'nom'): 'e',
            ('schwach', 'plur', 'acc'): 'e',
            ('schwach', 'plur', 'dat'): 'e',
            ('schwach', 'plur', 'gen'): 'e',
            ('schwach', 'plur', 'nom'): 'e',
            ('stark', 'fem', 'acc'): '',
            ('stark', 'fem', 'dat'): 'e',
            ('stark', 'fem', 'gen'): 'e',
            ('stark', 'fem', 'nom'): '',
            ('stark', 'masc', 'acc'): '',
            ('stark', 'masc', 'dat'): 'e',
            ('stark', 'masc', 'gen'): 'e',
            ('stark', 'masc', 'nom'): 'e',
            ('stark', 'neut', 'acc'): 'e',
            ('stark', 'neut', 'dat'): 'e',
            ('stark', 'neut', 'gen'): 'e',
            ('stark', 'neut', 'nom'): 'e',
            ('stark', 'plur', 'acc'): 'e',
            ('stark', 'plur', 'dat'): 'e',
            ('stark', 'plur', 'gen'): 'e',
            ('stark', 'plur', 'nom'): 'e',
        }

        lows = [
            'Non', 'Okt', 'Sept', 'Sext', 'Quint', 'Quadr', 'Tr', 'B', 'M',
        ]
        units = [
            '', 'un', 'duo', 'tre', 'quattuor', 'quin', 'sex', 'sept', 'okto', 'novem',
        ]
        tens = [
            'dez', 'vigint', 'trigint', 'quadragint', 'quinquagint', 'sexagint',
            'septuagint', 'oktogint', 'nonagint',
        ]
        self.high_numwords = ["zent"] + self.gen_high_numwords(units, tens, lows)

    def to_cardinal(self, value):
        # Preserve explicit compound examples, whose spelling sometimes differs
        # from that of the individual digits in the same reference.
        if value in self.number_examples:
            return self.title(self.number_examples[value])
        if value < 0 and -value in self.number_examples:
            return self.title(self.negword + self.number_examples[-value])
        return super().to_cardinal(value)

    def merge(self, curr, next):
        ctext, cnum, ntext, nnum = curr + next
        if cnum == 1:
            if nnum in {100, 1000}:
                prefix = self.hundred_prefix if nnum == 100 else ""
                return prefix + ntext, nnum
            if nnum < 10 ** 6:
                return next
            ctext = "ei"
        if nnum > cnum:
            if nnum >= 10 ** 6:
                if cnum > 1 and ntext.endswith("e"):
                    ntext += "n"
                ctext += " "
            value = cnum * nnum
        else:
            if nnum < 10 < cnum < 100:
                if nnum == 1:
                    ntext = "ein"
                connector = "ed" if ctext.startswith("acht") else "e"
                ctext, ntext = ntext + connector, ctext
            elif cnum >= 10 ** 6:
                ctext += " "
            value = cnum + nnum
        return ctext + ntext, value

    def to_ordinal(self, value, declension):
        self.verify_ordinal(value)
        key = (declension["declension"], declension["gender"], declension["case"].lower())
        if key not in self.ordinal_endings:
            raise ValueError("Unknown ordinal declension: " + str(declension))
        root = self.ordinal_roots.get(value)
        if root is None:
            # Compound ordinals use the same irregular ending as their last unit.
            cardinal = self.to_cardinal(value).lower()
            unit = value % 100 if value % 100 < 20 else value % 10
            if (unit in self.ordinal_roots and unit < 20
                    and cardinal.endswith(self.number_examples[unit])):
                root = cardinal.removesuffix(self.number_examples[unit]) + self.ordinal_roots[unit]
            else:
                root = cardinal + ("scht" if value >= 20 else "t")
        return root + self.ordinal_endings[key]

    def to_lookup(self, val):
        if val == "sek":
            return self.second_word

    def to_year(self, val, longval=True):
        if not (val // 100) % 10:
            return self.to_cardinal(val)
        return self.to_splitnum(
            val, hightxt=self.mid_numwords[1][1], longval=longval
        ).replace(" ", "")

    def to_ordinal_num(self, value):
        self.verify_ordinal(value)
        return str(value) + "."

    def to_currency(self, val, currency='EUR', cents=True, separator=' und',
                    adjective=False):
        result = super().to_currency(
            val, currency=currency, cents=cents, separator=separator,
            adjective=adjective)
        # Handle exception, in german is "ein Euro" and not "eins Euro"
        return result.replace("eis ", "ei ")

    def to_minutes(self, val):
        if val in self.minutes:
            return self.minutes[val]
        elif val < 30:
            return self.to_cardinal(val) + " ab"
        elif (val > 30) and (val < 60):
            return self.to_cardinal(60 - val) + " vor"

    def to_hours(self, val):
        if val in self.hours:
            return self.hours[val]

    def to_month_dates(self, val):
        if val in self.month_dates:
            return self.month_dates[val]
