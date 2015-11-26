"""
A module for generating well-formatted truth tables, using object-oriented
design patterns.
"""

from abc import ABCMeta, abstractmethod

__all__ = []

class GenericFormatter(object):
    __metaclass__ = ABCMeta
    
    def __init__(self, raw_eq_in):
        self.raw_eq = raw_eq_in
    
    def __str__(self):
        # TODO
        # this is where we will generate the array of values
        pass
    
    def __repr__(self):
        # TODO
        pass
    
    def __unicode__(self):
        # TODO
        pass
    
    def extract_symbols(self):
        """Returns a list of the symbols in the passed Boolean equation.
        All symbols are assumed to be uppercase and one character. 
        All other characters are discarded in the processing of the equation.
        The first symbols in the list is the result of the equation.
        """
        # TODO: more advanced logic in determining valid symbols
        return [sym for sym in self.equation if sym.isalnum() and sym.isupper()]
    
    @abstractmethod
    def make_table(self):
        pass

class TruthTableFormatter(GenericFormatter):
    def make_table(self):
        # TODO
        pass
    
class KMapFormatter(GenericFormatter):
    def make_table(self):
        # TODO
        pass