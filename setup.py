import os

from setuptools import find_packages
from setuptools import setup

##################################################
# Dependencies
##################################################

PYTEST_VERSION_ = '5.2.3'

# Packages required in 'production'
REQUIRED = [
    'tqdm==4.39.0',
    'num2words==0.5.10',
]

# Packages required for dev/ci enrionment
EXTRAS = {
    'dev': [
        'click==7.0',
        'pytest==%s' % (PYTEST_VERSION_,),
        'pytest-runner==5.2',
        'pytest-cov==2.8.1',
        'pytest-benchmark==3.2.2',
        'bump2version'
    ],
    'ci': [
        'flake8==3.7.9',
        'flake8-quotes==2.1.1'
    ],
}

# Packages required for testing
TESTS = [
    'pytest==%s' % (PYTEST_VERSION_,),
    'requests_mock==1.7.0'
]

##################################################
# Description
##################################################

DESCRIPTION = 'spoteno is a library for spoken text normalization for ASR'

root = os.path.abspath(os.path.dirname(__file__))
readme_path = os.path.join(root, 'README.md')

# Import the README and use it as the long-description.
try:
    with open(readme_path, encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

##################################################
# SETUP
##################################################

setup(name='spoteno',
      version='0.1.1',
      description=DESCRIPTION,
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/ynop/spoteno',
      download_url='https://github.com/ynop/spoteno/releases',
      author='Matthias Buechi',
      author_email='buec@zhaw.ch',
      classifiers=[
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3 :: Only',
          'Topic :: Scientific/Engineering :: Human Machine Interfaces'
      ],
      keywords='ASR speech recognition spoken text normalization transcripts',
      license='MIT',
      packages=find_packages(exclude=['tests']),
      install_requires=REQUIRED,
      include_package_data=True,
      zip_safe=False,
      test_suite='tests',
      extras_require=EXTRAS,
      setup_requires=['pytest-runner'],
      tests_require=TESTS,
      entry_points={}
      )
