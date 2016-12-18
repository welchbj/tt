from __future__ import print_function

import codecs
import os
import re
import sys

try:
    from setuptools import setup, find_packages
except ImportError:
    print('setuptools is required for tt installation.\n'
          'You can install it using pip.', file=sys.stderr)
    sys.exit(1)

here = os.path.abspath(os.path.dirname(__file__))
tt_dir = os.path.join(here, 'tt')

tt_pypi_name = 'ttable'
tt_description = ('A library and command-line tool for working with Boolean '
                  'expressions')
tt_license = 'MIT'
tt_author = 'Brian Welch'
tt_author_email = 'welch18@vt.edu'
tt_url = 'https://github.com/welchbj/tt'
tt_install_requires = []  # no dependencies. Wow!

version_pattern = re.compile(r'__version__\s+=\s+(.*)')
with codecs.open(os.path.join(tt_dir, 'core.py'),
                 encoding='utf-8') as f:
    tt_version = version_pattern.search(f.read()).group(1)

with codecs.open(os.path.join(here, 'README.rst'),
                 encoding='utf-8') as f:
    tt_long_description = f.read()

tt_entry_points = {
    'console_scripts': ['tt = tt.__main__:main']
}

tt_classifiers = [
    'Environment :: Console',
    'License :: OSI Approved :: MIT License',
    'Operating System :: MacOS :: MacOS X',
    'Operating System :: Microsoft :: Windows',
    'Operating System :: POSIX',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Topic :: Utilities'
]

setup(
    name=tt_pypi_name,
    version=tt_version,
    description=tt_description,
    long_description=tt_long_description,
    author=tt_author,
    author_email=tt_author_email,
    url=tt_url,
    license=tt_license,
    install_requires=tt_install_requires,
    packages=find_packages(exclude=['tests', '*.tests', '*.tests.*']),
    entry_points=tt_entry_points,
    classifiers=tt_classifiers
)
