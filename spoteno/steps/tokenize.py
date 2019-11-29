import re


class WhitespaceTokenize:

    def run(self, token):
        return list(re.split(r'\s+', token))
