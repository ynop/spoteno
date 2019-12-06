import functools
import multiprocessing
from tqdm import tqdm

from spoteno.configuration import de


class Normalizer:
    """
    This is the main class of spoteno.
    The normalizer processes text-sentences based on a specific configuration.
    A configuration defines steps and valid output symbols.

    Args:
        configuration (Configuration): The configuration to use.
        num_workers (int): Number of processes to use.
        log (bool): If ``True``, the result of every step is printed.
    """

    def __init__(self, configuration, num_workers=4, log=False):
        self.config = configuration
        self.num_workers = num_workers
        self.log = log

    def normalize_list(self, sentences, force=True):
        """
        Normalize the given sentences and return them.

        Args:
            sentences (list): The list of input sentences.
            force (bool): If ``True``, any invalid character remaining
                          after all steps is deleted with no replacement.
                          If ``False``, the output may contain
                          invalid characters.
        Return:
            list: The normalized sentences.
        """
        normalized = []

        if self.num_workers > 1:
            with multiprocessing.Pool(self.num_workers) as p:
                func = functools.partial(
                    self.normalize,
                    force=force
                )

                normalized = list(tqdm(
                    p.imap(func, sentences),
                    total=len(sentences)
                ))
        else:
            normalized = [self.normalize(s) for s in sentences]

        return normalized

    def normalize(self, sentence, force=True):
        """
        Normalize and return a single sentence.

        Args:
            sentence (str): The input sentence.
            force (bool): If ``True``, any invalid character remaining
                          after all steps is deleted with no replacement.
                          If ``False``, the output may contain
                          invalid characters.
        Return:
            str: The normalized sentence.
        """
        tokens = [sentence]

        if self.log:
            print('{:<20}{}'.format('START', sentence))

        for step in self.config.steps:
            out_tokens = []

            for token in tokens:
                step_tokens = step.run(token)
                out_tokens.extend(step_tokens)

            if self.log:
                print('{:<20}{}'.format(step.__class__.__name__, out_tokens))

            tokens = out_tokens

        if force:
            force_cleaned = []

            for t in tokens:
                clean_token = self.remove_all_invalid_characters(t)
                force_cleaned.append(clean_token)

            tokens = force_cleaned

        tokens = [t.strip() for t in tokens]
        tokens = [t for t in tokens if len(t) > 0]

        if self.log:
            print('{:<20}{}'.format('END', tokens))

        return ' '.join(tokens)

    def debug_list(self, sentences):
        """
        Same as ``debug()``, but processes a list of sentences.
        """
        result = []

        if self.num_workers > 1:
            with multiprocessing.Pool(self.num_workers) as p:
                result = list(tqdm(
                    p.imap(self.debug, sentences),
                    total=len(sentences)
                ))
        else:
            result = [self.debug(s) for s in sentences]

        return result

    def debug(self, sentence):
        """
        As well as ``normalize()`` the sentence is normalized.
        But in addition a set of characters is returned,
        which are not normalized with the given configuration.
        This is useful when building up a new configuration.
        """
        output = self.normalize(sentence, force=False)
        invalid_characters = set()

        for c in output:
            if c not in self.config.valid_characters:
                invalid_characters.add(c)

        return output, invalid_characters

    def remove_all_invalid_characters(self, text):
        clean = [c for c in text if c in self.config.valid_characters]
        return ''.join(clean)

    @classmethod
    def de(cls, lower_case=True, **kwargs):
        """ German configuration """
        de_configuration = de.build(lower_case=lower_case)
        return cls(de_configuration, **kwargs)
