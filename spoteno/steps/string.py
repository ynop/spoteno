import re


class Strip:

    def run(self, token):
        return [token.strip()]


class StripChar:

    def __init__(self, chars):
        self.chars = chars

    def run(self, token):
        while len(token) > 0 and token[0] in self.chars:
            token = token[1:]

        while len(token) > 0 and token[-1] in self.chars:
            token = token[:-1]

        return [token]


class Lower:

    def run(self, token):
        return [token.lower()]


class Delete:

    def __init__(self, chars):
        self.chars = chars

    def run(self, token):
        for c in self.chars:
            token = token.replace(c, '')

        return [token]
