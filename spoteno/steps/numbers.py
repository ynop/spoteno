import re
import num2words


INT_PATTERN = re.compile(r'^-?[0-9]+$')
FLOAT_PATTERN = re.compile(r'^-?[0-9]+[,\.][0-9]+$')

ORDINAL_PATTERN = re.compile(r'^[0-9]+\.?$')
NUM_PATTERN = re.compile(r'^-?[0-9]+([,\.][0-9]+$)?')


class NumberToWords:

    def __init__(self, lang_code):
        self.lang_code = lang_code

    def run(self, token):
        float_match = FLOAT_PATTERN.match(token)

        if float_match is not None:
            out = []

            if token.startswith('-'):
                out.append('minus')
                token = token[1:]

            num_word = num2words.num2words(
                float(token.replace(',', '.')),
                lang=self.lang_code
            ).lower()

            out.extend(num_word.split(' '))
            return out

        int_match = INT_PATTERN.match(token)

        if int_match is not None:
            out = []

            if token.startswith('-'):
                out.append('minus')
                token = token[1:]

            num_word = num2words.num2words(
                int(token.replace(',', '.')),
                lang=self.lang_code
            ).lower()

            out.extend(num_word.split(' '))
            return out

        return [token]


class OrdinalNumberToWords:

    def __init__(self, lang_code):
        self.lang_code = lang_code

    def run(self, token):
        match = ORDINAL_PATTERN.match(token)

        if match is not None:
            num_word = num2words.num2words(
                int(token[:-1]),
                lang=self.lang_code,
                to='ordinal'
            ).lower()
            return num_word.split(' ')

        return [token]


class SplitNumberSuffix:
    """
    If any of the given strings is directly connected to
    a number it is separated.

    "2000%" -> "2000" "%"
    But not "2000%ff"
    """

    def __init__(self, suffixes):
        self.suffixes = sorted(suffixes, reverse=True)

    def run(self, token):
        for s in self.suffixes:
            if token.endswith(s):
                should_be_number = token[:-len(s)]
                match = NUM_PATTERN.match(should_be_number)

                if match is not None:
                    return [token[:-len(s)], token[-len(s):]]

        return [token]
