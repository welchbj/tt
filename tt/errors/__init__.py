"""tt error types."""

# import base exception types
from .base import TtError  # noqa
from .evaluation import EvaluationError  # noqa
# from .generic import TODO
from .grammar import GrammarError  # noqa
from .state import StateError  # noqa
# TODO: refactor error types and base errors

# import specific exception types
from .evaluation import (DuplicateSymbolError, ExtraSymbolError,  # noqa
                         InvalidBooleanValueError, MissingSymbolError,
                         NoEvaluationVariationError)
from .generic import (ConflictingArgumentsError, InvalidArgumentTypeError,  # noqa
                      InvalidArgumentValueError, RequiredArgumentError)
from .grammar import (BadParenPositionError, EmptyExpressionError,  # noqa
                      ExpressionOrderError, UnbalancedParenError)
from .state import AlreadyFullTableException  # noqa
