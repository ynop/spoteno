# spoteno

[![PyPI](https://img.shields.io/pypi/v/spoteno.svg)](https://pypi.python.org/pypi/spoteno)

spoteno (Spoken-Text-Normalization) is a tool to cleanup text-transcripts for speech recognition systems.
These systems normally expect target transcripts to contain only characters from a restricted set.

## Installation

Install the latest development version:

```sh
pip install git+https://github.com/ynop/spoteno.git
```

## Examples
The default usecase would be to normalize a sentence.
This enforces the output string to contain only valid characters (as defined by the configuration).

```python
import spoteno

sentence = ('Am 11. Januar geht er um 5m nach links,'
            'weshalb er $d schon "ziemlich" müde ist.')

norm = spoteno.Normalizer.de()
outsent = norm.normalize(sentence)
print(outsent)

# >>> am elfte januar geht er um fünf m nach links weshalb er d schon ziemlich müde ist
```

With ``force=False``, the final cleanup can be disabled.
This way invalid characters may occurr in the output,
if the configuration hasn't handled them specifically.
```python
outsent = norm.normalize(sentence, force=False)
print(outsent)

# >>> am elfte januar geht er um fünf m nach links weshalb er $d schon ziemlich müde ist
```

With the debug method, one can retrieve a set of invalid characters in the final output.
This can be used to create or debug a configuration.
Additionaly the outputs of the different configuration steps can be printed.
```python
outsent, error = norm.debug(sentence)
print(error)

# >>> START               Am 11. Januar geht er um 5m nach links,weshalb er $d schon "ziemlich" müde ist.
# >>> Strip               ['Am 11. Januar geht er um 5m nach links,weshalb er $d schon "ziemlich" müde ist.']
# >>> Lower               ['am 11. januar geht er um 5m nach links,weshalb er $d schon "ziemlich" müde ist.']
# >>> StripChar           ['am 11. januar geht er um 5m nach links,weshalb er $d schon "ziemlich" müde ist']
# >>> ReplaceIfNotSurroundedByDigits['am 11. januar geht er um 5m nach links weshalb er $d schon "ziemlich" müde ist']
# >>> ReplaceIfNotPrecededByDigit['am 11. januar geht er um 5m nach links weshalb er $d schon "ziemlich" müde ist']
# >>> ReplaceRegex        ['am 11. januar geht er um 5m nach links weshalb er $d schon "ziemlich" müde ist']
# >>> ReplaceChar         ['am 11. januar geht er um 5m nach links weshalb er $d schon  ziemlich  müde ist']
# >>> ReplaceChar         ['am 11. januar geht er um 5m nach links weshalb er $d schon  ziemlich  müde ist']
# >>> WhitespaceTokenize  ['am', '11.', 'januar', 'geht', 'er', 'um', '5m', 'nach', 'links', 'weshalb', 'er', '$d', 'schon', 'ziemlich', 'müde', 'ist']
# >>> SplitNumberSuffix   ['am', '11.', 'januar', 'geht', 'er', 'um', '5', 'm', 'nach', 'links', 'weshalb', 'er', '$d', 'schon', 'ziemlich', 'müde', 'ist']
# >>> NumberToWords       ['am', '11.', 'januar', 'geht', 'er', 'um', 'fünf', 'm', 'nach', 'links', 'weshalb', 'er', '$d', 'schon', 'ziemlich', 'müde', 'ist']
# >>> OrdinalNumberToWords['am', 'elfte', 'januar', 'geht', 'er', 'um', 'fünf', 'm', 'nach', 'links', 'weshalb', 'er', '$d', 'schon', 'ziemlich', 'müde', 'ist']
# >>> ReplaceChar         ['am', 'elfte', 'januar', 'geht', 'er', 'um', 'fünf', 'm', 'nach', 'links', 'weshalb', 'er', '$d', 'schon', 'ziemlich', 'müde', 'ist']
# >>> ReplaceFull         ['am', 'elfte', 'januar', 'geht', 'er', 'um', 'fünf', 'm', 'nach', 'links', 'weshalb', 'er', '$d', 'schon', 'ziemlich', 'müde', 'ist']
# >>> RemoveDiacritics    ['am', 'elfte', 'januar', 'geht', 'er', 'um', 'fünf', 'm', 'nach', 'links', 'weshalb', 'er', '$d', 'schon', 'ziemlich', 'müde', 'ist']
# >>> Strip               ['am', 'elfte', 'januar', 'geht', 'er', 'um', 'fünf', 'm', 'nach', 'links', 'weshalb', 'er', '$d', 'schon', 'ziemlich', 'müde', 'ist']
# >>> END                 ['am', 'elfte', 'januar', 'geht', 'er', 'um', 'fünf', 'm', 'nach', 'links', 'weshalb', 'er', '$d', 'schon', 'ziemlich', 'müde', 'ist']k

# >>> {'$'}
```

## Development

### Prerequisites

* [A supported version of Python 3](https://docs.python.org/devguide/index.html#status-of-python-branches)

It's recommended to use a virtual environment when developing spoteno.
To create one, execute the following command in the project's root directory:

```
python -m venv .
```

To install spoteno and all it's dependencies, execute:

```
pip install -e .
```

### Running the test suite

```
pip install -e .[dev]
python setup.py test
```

With PyCharm you might have to change the default test runner. Otherwise, it might only suggest to use nose. To do so,
go to File > Settings > Tools > Python Integrated Tools (on the Mac it's PyCharm > Preferences > Settings > Tools >
Python Integrated Tools) and change the test runner to py.test.


### Versions

Versions is handled using [bump2version](https://github.com/c4urself/bump2version). To bump the version:

```
bump2version [major,minor,patch,release,num]
```

In order to directly go to a final relase version (skip .dev/.rc/...):

```
bump2version [major,minor,patch] --new-version x.x.x
```

### Release

Commands to create a new release on pypi.

```
rm -rf build
rm -rf dist

python setup.py sdist
python setup.py bdist_wheel
twine upload dist/*
```
