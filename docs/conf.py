import os
import sys

from datetime import datetime


HERE = os.path.dirname(os.path.abspath(__file__))
DOCS_DIR = os.path.dirname(HERE)
BASE_DIR = os.path.dirname(DOCS_DIR)
TT_MODULE_DIR = os.path.join(BASE_DIR, 'tt')
sys.path.insert(0, TT_MODULE_DIR)

extensions = ['sphinx.ext.autodoc',
              'sphinx.ext.napoleon',
              'sphinx.ext.viewcode']

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
    'fixed_sidebar': True
}

exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
templates_path = ['_templates']
html_static_path = ['_static']

project = 'tt'
year = datetime.now().year
author = 'Brian Welch'
copyright = '{}, {}'.format(year, author)
version = '0.4'
release = '0.4.1'
master_doc = 'index'
source_suffix = '.rst'
pygments_style = 'sphinx'
