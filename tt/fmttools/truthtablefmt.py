"""
A module for generating well-formatted truth tables.
"""

def get_title_row(col_titles, delim="|"):
    """Constructs a string of the table's title row.
    """
    return delim + [col_title + delim for col_title in col_titles]