"""tt error types."""

# import base exception types
from .arguments import ArgumentError  # noqa
from .base import TtError  # noqa
from .evaluation import EvaluationError  # noqa
from .grammar import GrammarError  # noqa
from .state import StateError  # noqa
from .symbols import SymbolError  # noqa

# import specific exception types
from .arguments import (ConflictingArgumentsError, InvalidArgumentTypeError,  # noqa
                        InvalidArgumentValueError, RequiredArgumentError)
from .evaluation import InvalidBooleanValueError, NoEvaluationVariationError  # noqa
from .grammar import (BadParenPositionError, EmptyExpressionError,  # noqa
                      ExpressionOrderError, InvalidIdentifierError,
                      UnbalancedParenError)
from .state import AlreadyFullTableError, RequiresFullTableError  # noqa
from .symbols import DuplicateSymbolError, ExtraSymbolError, MissingSymbolError  # noqa
