import re


class ReplaceChar:

    def __init__(self, mapping):
        self.mapping = mapping

    def run(self, token):
        for x, y in self.mapping.items():
            token = token.replace(x, y)

        return [token]


class ReplaceFull:

    def __init__(self, mapping):
        self.mapping = mapping

    def run(self, token):
        if token in self.mapping.keys():
            return [self.mapping[token]]

        return [token]


class ReplaceRegex:

    def __init__(self, mapping):
        self.mapping = mapping

    def run(self, token):
        for x, y in self.mapping.items():
            token = re.sub(x, y, token)

        return [token]


class ReplaceIfNotSurroundedByDigits:
    """
    Replace char if a digit is not on both sides of the char.
    """

    def __init__(self, chars):
        self.chars = chars
        self.digit_pattern = re.compile(r'^\d$')

    def run(self, token):
        for char, replace_with in self.chars.items():
            # Find all occurences of char
            matches = re.finditer(re.escape(char), token)

            for m in matches:
                left_match = self.digit_pattern.match(
                    token[m.start()-1: m.start()])
                right_match = self.digit_pattern.match(
                    token[m.end(): m.end()+1])

                # Replace if either no digit on the left or on the right
                if left_match is None or right_match is None:
                    token = token[:m.start()] + replace_with + token[m.end():]

        return [token]


class ReplaceIfNotPrecededByDigit:
    """
    Replace char if no digit is in front of char.
    """

    def __init__(self, chars):
        self.chars = chars
        self.digit_pattern = re.compile(r'^\d$')

    def run(self, token):
        for char, replace_with in self.chars.items():
            # Find all occurences of char
            matches = re.finditer(re.escape(char), token)

            for m in matches:
                left_match = self.digit_pattern.match(
                    token[m.start()-1: m.start()])

                # Replace if no digit on the left
                if left_match is None:
                    token = token[:m.start()] + replace_with + token[m.end():]

        return [token]
