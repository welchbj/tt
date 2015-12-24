import codecs
import re
import sys
import os

try:
    from setuptools import setup, find_packages
except ImportError:
    print('setuptools is required for tt installation.\n'
          'You can install it using pip.')
    sys.exit(1)

here = os.path.abspath(os.path.dirname(__file__))
tt_dir = os.path.join(here, 'tt')

tt_pypi_name = 'ttable'
tt_description = 'Command line tool for Boolean algebra operations'
tt_license = 'MIT'
tt_author = 'Brian Welch'
tt_url = 'https://github.com/welchbj/tt'

version_pattern = re.compile(r'__version__\s+=\s+(.*)')
with codecs.open(os.path.join(tt_dir, 'core.py'), encoding='utf-8') as f:
    tt_version = version_pattern.search(f.read()).group(1)

with codecs.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    tt_long_description = f.read()

tt_install_requires = [
    'pip >= 1.4'
    'setuptools >= 0.8'
]

tt_doc_extras = [
    'sphinx >= 1.3' # napoleon
]

tt_dev_extras = tt_doc_extras + [
    'flake8',
    'wheel'
]

tt_classifiers = [
    'Environment :: Console',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5'
]


setup(
    name=tt_pypi_name,
    version=tt_version,
    description=tt_description,
    long_description=tt_long_description,
    author=tt_author,
    url=tt_url,
    license=tt_url,
    install_requires=tt_install_requires,
    extras_require={
        'doc': tt_doc_extras,
        'development': tt_doc_extras
    },
    packages=find_packages(),
    entry_points={
        'console_scripts':
            ['tt = tt.__main__:main']
    },
    classifiers=tt_classifiers
)
