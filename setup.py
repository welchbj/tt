from __future__ import print_function

import codecs
import os
import sys

try:
    from setuptools import Extension, find_packages, setup
except ImportError:
    print('setuptools is required for tt installation.\n'
          'You can install it using pip.', file=sys.stderr)
    sys.exit(1)

# directories/files
here = os.path.abspath(os.path.dirname(__file__))
readme_file = os.path.join(here, 'README.rst')
tt_dir = os.path.join(here, 'tt')

clibs_dir = os.path.join(tt_dir, '_clibs')
cli_dir = os.path.join(tt_dir, 'cli')
version_file = os.path.join(tt_dir, 'version.py')

# setup kwarg values
tt_pypi_name = 'ttable'
tt_description = ('A library and command-line tool for working with Boolean '
                  'expressions')
tt_license = 'MIT'
tt_author = 'Brian Welch'
tt_author_email = 'welch18@vt.edu'
tt_url = 'http://tt.bwel.ch'
tt_install_requires = []  # no dependencies. Wow!

with codecs.open(version_file, encoding='utf-8') as f:
    exec(f.read())  # loads __version__ and __version_info__
    tt_version = __version__  # noqa

with codecs.open(readme_file, encoding='utf-8') as f:
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
    'Programming Language :: Python :: Implementation :: CPython',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Topic :: Utilities'
]

# C-extension config
picosat_ext_config = dict(
    define_macros=[
        ('NDEBUG', None)
    ],
    include_dirs=[
        os.path.join(clibs_dir, 'picosat')
    ],
    sources=[
        os.path.join(clibs_dir, 'picosat', 'picosat.c'),
        os.path.join(clibs_dir, 'picosatmodule.c')
    ]
)

if sys.platform == 'win32':
    picosat_ext_config['define_macros'] += [
        ('NGETRUSAGE', None),
        ('inline', '__inline')
    ]

picosat = Extension('tt._clibs.picosat', **picosat_ext_config)

if os.environ.get('READTHEDOCS') == 'True':
    # don't build C-extensions on ReadTheDocs
    tt_extensions = []
else:
    tt_extensions = [picosat]

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
    classifiers=tt_classifiers,
    ext_modules=tt_extensions
)
