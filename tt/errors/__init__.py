"""tt error types."""

# import base exception types
from .arguments import ArgumentError
from .base import TtError
from .evaluation import EvaluationError
from .grammar import GrammarError
from .state import StateError
from .symbols import SymbolError

# import specific exception types
from .arguments import (
    ConflictingArgumentsError,
    InvalidArgumentTypeError,
    InvalidArgumentValueError,
    RequiredArgumentError,
)
from .evaluation import (
    InvalidBooleanValueError,
    NoEvaluationVariationError,
)
from .grammar import (
    BadParenPositionError,
    EmptyExpressionError,
    ExpressionOrderError,
    InvalidIdentifierError,
    UnbalancedParenError,
)
from .state import (
    AlreadyConstrainedSymbolError,
    AlreadyFullTableError,
    RequiresFullTableError,
    RequiresNormalFormError,
)
from .symbols import (
    DuplicateSymbolError,
    ExtraSymbolError,
    MissingSymbolError,
)
