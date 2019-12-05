from spoteno import resources

import spoteno
from spoteno import steps


def build(lower_case=True):
    """
    Normalizer for german.
    """
    valid_characters = resources.load_valid_characters('de')
    pipeline = []

    # Strip the input
    pipeline.append(steps.Strip())

    # All to lower case
    if lower_case:
        pipeline.append(steps.Lower())

    # Strip . at the begin/end of the input
    # Since we assume input is a sentence
    pipeline.append(steps.StripChar([
        '.',
    ]))

    # Remove commas, if not used for a floating number
    pipeline.append(steps.ReplaceIfNotSurroundedByDigits({
        ',': ' ',
    }))

    # Remove points, if not used for a floating number
    # or an ordinal
    pipeline.append(steps.ReplaceIfNotPrecededByDigit({
        '.': ' ',
    }))

    pipeline.append(steps.ReplaceRegex({
        # "'([^s])": r'\1',  # Only keep ' with 's (e.g. hat's)
    }))

    # Remove punctuation, that most likely has no influence
    pipeline.append(steps.ReplaceChar({
        '–': ' ',
        '-': ' ',
        '—': ' ',
        '−': ' ',
        '_': ' ',
        '?': ' ',
        '!': ' ',
        ':': ' ',
        ';': ' ',
        '“': ' ',
        '„': ' ',
        '”': ' ',
        ')': ' ',
        '(': ' ',
        '«': ' ',
        '»': ' ',
        '’': ' ',
        '‚': ' ',  # Not a komma
        '‹': ' ',
        '›': ' ',
        '‘': ' ',
        '^': ' ',
        '"': ' ',
        '­': ' ',  # \xad some space
        '´': '',
        "'": ''
    }))

    # Can go wrong
    #
    #   e.g. 'm / s' -> should be meter PRO sekunde
    #
    pipeline.append(steps.ReplaceChar({
        '/': ' ',
    }))

    # Tokenize words
    pipeline.append(steps.WhitespaceTokenize())

    # Separate Suffixes from numbers if there is no space
    pipeline.append(steps.SplitNumberSuffix([
        '%',
        '‰',
        'º',
        '°',
        'm',
    ]))

    # Convert numbers to words
    pipeline.append(steps.NumberToWords('de'))
    pipeline.append(steps.OrdinalNumberToWords('de'))

    # Replace character with ss
    pipeline.append(steps.ReplaceChar({'ß': 'ss', }))

    # Replace common abbreviations, shortforms, etc
    pipeline.append(steps.ReplaceFull({
        '%': 'prozent',
        '‰': 'promille',
        '§': 'paragraph',
        '±': 'plus minus',
        '&': 'und',
        'ºc': 'grad celsius',
        '°c': 'grad celsius',
        'º': 'grad',
        '°': 'grad',
        'kg': 'kilogramm',
        'α': 'alpha',
        'β': 'beta',
        'γ': 'gamma',
        'km²': 'quadrat kilometer',
        'm²': 'quadrat meter',
        'm³': 'kubik meter',
        'cm²': 'quadrat zentimeter',
        'cm³': 'kubik zentimeter',
        'co2': 'co zwei',
        '3d': 'drei d',
        'g20': 'g zwanzig',
        'g7': 'g sieben',
        'g8': 'g acht',
        '3g': 'drei g',
        '5g': 'fünf g',
        '1940er': 'neunzehn hundert vierziger',
        '1950er': 'neunzehn hundert fünfziger',
        '1960er': 'neunzehn hundert sechziger',
        '1970er': 'neunzehn hundert siebziger',
        '1980er': 'neunzehn hundert achtziger',
        '1990er': 'neunzehn hundert neunziger',
        '50er': 'fünfziger',
        '60er': 'sechziger',
        '70er': 'siebziger',
        '80er': 'achtziger',
        '90er': 'neunziger',
        'a320': 'a drei hundert zwanzig'

    }))

    # Remove Diacritics (e.g. à -> a)
    pipeline.append(steps.RemoveDiacritics(valid_characters))

    # Strip tokens
    pipeline.append(steps.Strip())

    return spoteno.Configuration(pipeline, valid_characters)
