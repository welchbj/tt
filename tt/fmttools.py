"""Generation of formatted truth tables, using object-oriented design patterns.
"""

import itertools

from tt.eqtools import get_symbol_input_array

__all__ = ["TruthTablePrinter"]

DEFAULT_TABLE_CELL_PADDING_WIDTH = 1


class TruthTablePrinter(object):
    """Printer of nice looking truth tables.

    Attributes:
        eval_result_wrapper (EvaluationResultWrapper): An instance containing
            the results that will be printed within the table.
        table_cell_padding_width (int): The minimum blank space to the left
            and right of each cell's contents in the table.

    """
    def __init__(self, eval_result_wrapper,
                 table_cell_padding_width=DEFAULT_TABLE_CELL_PADDING_WIDTH):
        self.eval_result_wrapper = eval_result_wrapper
        self.table_cell_padding_width = table_cell_padding_width

    def get_column_width_list(self):
        """Get information on the width of each column of the table.

        Notes:
            Take into account cell padding but not column separators.

        Returns:
            List[int]: The width of each column.

        """
        cell_padding = 2*self.table_cell_padding_width
        input_symbol_column_widths = [
            cell_padding + len(symbol) for symbol in
            self.eval_result_wrapper.input_symbols]
        output_symbol_column_width = (
            cell_padding + len(self.eval_result_wrapper.output_symbol))
        return input_symbol_column_widths + [output_symbol_column_width]

    def get_fancy_row_separator(self):
        """Get the separator for important row changes in the table.

        Returns:
            str: The fancy row separator, in the style "+---+---+".

        """
        return "+" + "+".join("-" * col_width
                              for col_width
                              in self.get_column_width_list()) + "+"

    def table_rowify(self, items, sep="|"):
        """Transform the contents of items into a row of the table.

        Args:
            items List(str): The contents of each cell of the row.
            sep str: What to separate each row with. Assume to be length of 1.

        Returns:
            str: The table row.

        """
        row = sep
        for item, col_width in zip(items, self.get_column_width_list()):
            total_pad_len = col_width - len(item)
            left_pad_len = total_pad_len // 2
            right_pad_len = left_pad_len + int(total_pad_len % 2)
            row += left_pad_len * " "
            row += item
            row += right_pad_len * " "
            row += sep
        return row

    def print_tt(self):
        """Print the truth table.

        Print the table, row by row.

        Returns:
            None

        """
        fancy_row_sep = self.get_fancy_row_separator()

        input_symbols = self.eval_result_wrapper.input_symbols
        output_symbol = self.eval_result_wrapper.output_symbol

        title_row = self.table_rowify(
            itertools.chain(input_symbols, [output_symbol]))

        print(fancy_row_sep)
        print(title_row)
        print(fancy_row_sep)

        results = self.eval_result_wrapper.result_list
        for i, input_row in enumerate(get_symbol_input_array(input_symbols)):
            print(self.table_rowify(itertools.chain(input_row, results[i])))

        print(fancy_row_sep)
