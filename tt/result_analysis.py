"""A module used for transforming evaluation results into different forms.
"""


# define what symbols are used in sop/pos output representation
OUT_SYM_NOT = '~'
OUT_SYM_AND = ' and '
OUT_SYM_OR = ' or '


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


def dec_to_bool_list(num, tot_chars=None):
    result = bin(num)[2:]

    if tot_chars is not None:
        fill = '0' * (tot_chars-len(result))
        result = fill + result

    result_as_bool_list = [c == '1' for c in result]
    return result_as_bool_list
