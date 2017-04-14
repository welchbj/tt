import codecs
import os
import sys

from datetime import datetime


HERE = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(HERE)
TT_MODULE_DIR = os.path.join(BASE_DIR, 'tt')
TT_VERSION_FILE = os.path.join(TT_MODULE_DIR, 'version.py')
sys.path.insert(0, BASE_DIR)

with codecs.open(TT_VERSION_FILE, encoding='utf-8') as f:
    exec(f.read())  # loads __version__ and __version_info__

extensions = ['sphinx.ext.autodoc',
              'sphinx.ext.intersphinx',
              'sphinx.ext.viewcode']

intersphinx_mapping = {'python': ('https://docs.python.org/3', None)}

autodoc_default_flags = ['members',
                         'special-members',
                         'show-inheritance']

suppress_warnings = ['image.nonlocal_uri']

html_theme = 'alabaster'
html_sidebars = {
    '**': [
        'about.html',
        'navigation.html',
        'relations.html',
        'searchbox.html'
    ]
}
html_theme_options = {
    'logo': 'logo.png',
    'logo_text_align': 'centered',
    'description': 'the Boolean expression toolbox',

    'github_user': 'welchbj',
    'github_repo': 'tt',
    'github_type': 'star',

    'extra_nav_links': {},
    'sidebar_includehidden': True,
    'fixed_sidebar': False,

    'warn_bg': '#f9e3ed',
    'warn_border': '#ffa5ce',
    'note_bg': '#e8f0fc',
    'note_border': '#c4daff',
    'pre_bg': '#f9f4fc',

    'font_family': "'PT Sans Caption', sans-serif",
    'font_size': '0.9em',
    'head_font_family': "'Cabin', sans-serif"
}

exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
templates_path = ['_templates']
html_static_path = ['_static']

project = 'tt'
year = datetime.now().year
author = 'Brian Welch'
copyright = '{}, {}'.format(year, author)
version = '.'.join(str(i) for i in __version_info__[:2])  # noqa
release = __version__  # noqa
master_doc = 'index'
source_suffix = '.rst'
pygments_style = 'sphinx'
