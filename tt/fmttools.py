"""Generation of formatted truth tables and Karnuagh Maps.
"""
from __future__ import print_function, division

import itertools
import math

from tt.bittools import (get_nth_gray_code, get_bit_string,
                         get_int_concatenation)
from tt.eqtools import get_symbol_input_array

DEFAULT_PADDING_WIDTH = 1


# === Shared Functionality ====================================================
def get_fancy_row_separator(col_widths):
    """Get the separator for important row changes in the table.

    Args:
        col_widths (List[int]): The width of each column to be printed in the
            row (i.e., the number of ``-``s to include).

    Returns:
        str: The fancy row separator, in the style ``+---+---+``.

    """
    return '+' + '+'.join('-' * col_width for col_width in col_widths) + '+'


def get_width_list(items, width_padding):
    """Get a list of the widths corresponding to ``items``, adjusted by
    ``width_padding``.

    Args:
        items (List): A list of objects upon which ``len`` can be called.
        width_padding (int): The padding to on either side of each element in
            ``items``.

    Returns:
        List[int]: The adjusted length of each element in ``items``.

    """
    pad = 2 * width_padding
    width_list = [(pad + len(elt)) for elt in items]
    return width_list


def table_rowify(items, col_widths, sep='|'):
    """Transform the contents of items into a row of the table.

    Args:
        items List(str): The contents of each cell of the row.
        sep (str): What to separate each row with. Assume to be length of 1.

    Returns:
        str: The table row.

    """
    row = sep
    for item, col_width in zip(items, col_widths):
        total_pad_len = col_width - len(item)
        left_pad_len = total_pad_len // 2
        right_pad_len = total_pad_len - left_pad_len
        row += (left_pad_len*' ' + item + right_pad_len*' ' + sep)
    return row


# === Truth Table Formatting ==================================================
def print_tt(eval_result,
             width_padding=DEFAULT_PADDING_WIDTH):
    """Print a truth table from an ``EvaluationResultWrapper`` instance.

    Args:
        eval_result (EvaluationResultWrapper): The result from which to pull
            the contents of the table.
        width_padding (int): The minimum empty space between the contents of
            each cell of the table and its cell "walls".

    Returns:
        None

    """
    title_row_items = eval_result.input_symbols + [eval_result.output_symbol]

    col_widths = get_width_list(title_row_items, width_padding)
    row_sep = get_fancy_row_separator(col_widths)

    print(row_sep)
    print(table_rowify(title_row_items, col_widths))
    print(row_sep)

    input_symbols = eval_result.input_symbols
    for i, input_row in enumerate(get_symbol_input_array(input_symbols)):
        print(
            table_rowify(
                itertools.chain(
                    input_row,
                    str(eval_result.result_list[i])), col_widths))

    print(row_sep)


# === Karnuagh Map Formatting =================================================
def print_kmap(input_vars, kmap_grid):
    """Print a Karnaugh Map.

    Args:
        input_vars (List[str]): The input variables of the equation which the
            printed Karnaugh Map is meant to represent.
        kmap_grid (List[List[KmapPoint]]): The grid containing the Boolean
            values with which to fill the printed Karnaugh Map.

    Returns:
        None

    Notes:
        This is designed to scale to an equation of any number of inputs
        greater than 1. Each box of the grid should remain a square and scale
        to the length of the Gray codes listed along the top of the Karnaugh
        map.

    """
    num_rows = len(kmap_grid)
    num_cols = len(kmap_grid[0])

    num_gcode_digits_row = int(math.log(num_rows, 2))
    num_gcode_digits_col = int(math.log(num_cols, 2))

    row_gcode_ints = [get_nth_gray_code(n) for n in range(num_rows)]
    col_gcode_ints = [get_nth_gray_code(n) for n in range(num_cols)]

    row_gcode_strs = [get_bit_string(n, num_chars=num_gcode_digits_row) for
                      n in row_gcode_ints]
    col_gcode_strs = [get_bit_string(n, num_chars=num_gcode_digits_col) for
                      n in col_gcode_ints]

    # base offset is the length of the row gray codes plus two spaces
    base_offset = num_gcode_digits_row + 2
    base_offset_str = base_offset*' '

    # we want at least a buffer of two spaces after the result in each box
    num_cols_per_box = (1 + num_gcode_digits_col +
                        max(2, 6 - num_gcode_digits_col))
    num_rows_per_box = num_cols_per_box // 2

    # indicate the ordering of variables in the gray codes
    print(' '.join(input_vars[:num_gcode_digits_row]),
          '\\',
          ' '.join(input_vars[num_gcode_digits_row:]))
    print()

    # making the top row of column gray codes
    num_spaces_btwn_top_row_gray_codes = (
        num_cols_per_box-(num_gcode_digits_col+1)+2)
    top_gcode_row = (
        (base_offset+2)*' ' +
        (num_spaces_btwn_top_row_gray_codes*' ').join(col_gcode_strs))
    print(top_gcode_row)

    box_widths = [num_cols_per_box] * num_cols
    row_sep = base_offset_str + get_fancy_row_separator(box_widths)

    # define row templates
    minterm_col_sep = '| {:<' + str(num_cols_per_box-1) + '}'
    minterm_row_template = (' {:' + str(num_gcode_digits_row) + '} ' +
                            minterm_col_sep*num_cols + '|')

    result_row_template = (base_offset_str +
                           table_rowify(itertools.repeat('{}', num_cols),
                                        [width+1 for width in box_widths]))

    empty_row = base_offset_str + table_rowify(
        itertools.repeat('', num_cols), box_widths)

    # determine the number of empty rows that will need to be printed for each
    # row of boxes
    num_rows_before_result_row = num_rows_per_box // 2
    num_rows_after_result_row = (num_rows_per_box - 1 -
                                 num_rows_before_result_row)

    # finally, construct the k map, stuffing results/gcodes into the templates
    print(row_sep)
    for i, row in enumerate(kmap_grid):
        r_gcode_str = row_gcode_strs[i]
        r_gcode_int = row_gcode_ints[i]
        curr_row_gcodes = [
            get_int_concatenation(r_gcode_int, c_gcode, num_gcode_digits_col)
            for c_gcode in col_gcode_ints]
        row_results = [kmap_point.val for kmap_point in row]

        print(minterm_row_template.format(r_gcode_str, *curr_row_gcodes))

        # subtract 1 to account for minterm row
        for x in range(num_rows_before_result_row-1):
            print(empty_row)

        print(result_row_template.format(*row_results))

        for x in range(num_rows_after_result_row):
            print(empty_row)

        print(row_sep)
