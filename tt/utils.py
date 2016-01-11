"""The functions that didn't fit anywhere else.
"""
from __future__ import print_function

import sys


def print_err(*args, **kwargs):
    print('ERROR:', *args, file=sys.stderr, **kwargs)


def without_spaces(the_str):
    return ''.join(the_str.split())


def matching_indices(the_list, search_val):
    return [pos for pos, val in enumerate(the_list) if val == search_val]
