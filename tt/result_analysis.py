"""A module used for transforming evaluation results into different forms.
"""

from collections import namedtuple

from tt.bittools import get_nth_gray_code, get_int_concatenation


class EquationTransformer(object):

    def __init__(self, bool_eq_wrapper):
        self.bool_eq_wrapper = bool_eq_wrapper

    def get_eq_from_expr(self, expr):
        return self.bool_eq_wrapper.output_symbol + ' = ' + expr

    def get_sop_form(self):
        pass

    def get_pos_form(self):
        pass

    def get_minimal_form(self):
        pass


def to_sop_form(high_indices, symbol_list):
    pass


def to_pos_form(low_indices, symbol_list):
    pass


def to_minimal_form():
    pass


KmapPoint = namedtuple('KmapPoint', ['gray_code', 'val'])


def eval_result_as_kmap_grid(eval_result):
    """Convert an ``EvaluationResultWrapper`` instance to a representation of a
    Karnuagh Map.

    Args:
        eval_result (EvaluationResultWrapper): The result instance which will
            be converted to a more intuitive representation of a Karnaugh Map.

    Returns:
        List[List[KmapPoint]]: A list array of ``KmapPoint``s, in row-by-row
            ordering according to increasing Gray Code.

    Raises:
        TooFewKarnaughMapInputs: Raise if less than 2 inputs are found in
            ``eval_result``.

    """
    num_vars = len(eval_result.input_symbols)

    if num_vars < 2:
        raise TooFewKarnaughMapInputs('Karnaugh Map generation requires an '
                                      'equation of at least 2 variables.')

    row_pow = num_vars // 2
    col_pow = row_pow + num_vars % 2

    num_rows = 2 ** row_pow
    num_cols = 2 ** col_pow

    kmap_grid = []

    col_gcodes = [get_nth_gray_code(n) for n in range(num_cols)]
    row_gcodes = col_gcodes[:num_rows]

    for i, row_gcode in enumerate(row_gcodes):
        kmap_grid.append([])
        for col_gcode in col_gcodes:
            gcode = get_int_concatenation(row_gcode, col_gcode, col_pow)
            kmap_point = KmapPoint(
                gray_code=gcode, val=eval_result.result_list[gcode])
            kmap_grid[i].append(kmap_point)

    return kmap_grid


class ExpandedKmapGrid(object):
    """Wraps a 2-D list representation of Karnaugh Map.

    For the optimization of POS and SOP forms.

    """

    def __init__(self, kmap):
        self.min_row = -len(kmap[0][0])
        self.min_col = 0
        self.max_row = 0
        self.max_col = 0

    def get_val(r, c):
        pass


class TooFewKarnaughMapInputs(Exception):
    """Error for when a Karnaugh Map is attempted with less than 2 inputs.

    """
    pass
