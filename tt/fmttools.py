"""
A module for generating well-formatted truth tables, using object-oriented
design patterns.
"""

import itertools
from eqtools import get_sym_input_array

__all__ = []

 # TODO: allow user to customize size of table/cells
DEFAULT_TABLE_CELL_PADDING_WIDTH = 1

class TruthTablePrinter(object):
    # assume all symbols are 1 character
    def __init__(self, eval_result_wrapper_in, table_cell_padding_width_in=DEFAULT_TABLE_CELL_PADDING_WIDTH):
        self.eval_result_wrapper = eval_result_wrapper_in
        self.table_cell_padding_width = table_cell_padding_width_in

    def get_column_width_list(self):
        # this will be useful when symbols are permitted to be wider than 1 character
        cell_padding = 2*self.table_cell_padding_width
        input_sym_column_widths = [cell_padding + len(sym) for sym in self.eval_result_wrapper.input_syms]
        output_sym_column_width = cell_padding + len(self.eval_result_wrapper.output_sym)
        return input_sym_column_widths + [output_sym_column_width]

    def get_fancy_row_separator(self):
        return "+" + "+".join("-" * col_width for col_width in self.get_column_width_list()) + "+"

    def table_rowify(self, items, sep="|"):
        pad = " " * self.table_cell_padding_width
        return sep + pad + (pad + sep + pad).join(items) + pad + sep

    def print_tt(self):
        fancy_row_sep = self.get_fancy_row_separator()

        input_syms = self.eval_result_wrapper.input_syms
        output_sym = self.eval_result_wrapper.output_sym
        title_row = self.table_rowify(itertools.chain(input_syms, output_sym))

        print(fancy_row_sep)
        print(title_row)
        print(fancy_row_sep)

        results = self.eval_result_wrapper.result_list
        for i, input_row in enumerate(get_sym_input_array(input_syms)):
            print(self.table_rowify(itertools.chain(input_row, results[i])))

        print(fancy_row_sep)
