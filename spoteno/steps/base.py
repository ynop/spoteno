

class Step:
    """
    The normalization process is split up into steps.
    The steps can be some specific implementations or
    generic processes (e.g. replacing characters).
    """

    def run(self, token):
        """
        Input is a single token.
        Return a list of tokens.
        """
        return [token]
