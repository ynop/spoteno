import unicodedata


class RemoveDiacritics:
    """
    Removes any diacritics if the resulting character
    is in the list of valid characters.
    """

    def __init__(self, valid_chars):
        self.valid_chars = valid_chars

    def run(self, token):
        chars = []

        for c in token:
            new_c = c

            if c not in self.valid_chars:
                decomposed = unicodedata.decomposition(c)
                decomposed = decomposed.split(' ')

                if len(decomposed) == 2:
                    try:
                        no_diac = chr(int(decomposed[0], 16))
                        if no_diac in self.valid_chars:
                            new_c = no_diac
                    except ValueError:
                        pass

            chars.append(new_c)

        return [''.join(chars)]
