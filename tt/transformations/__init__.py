"""Interfaces for transforming representations of expressions."""

from .bexpr import (  # noqa
    apply_de_morgans,
    apply_idempotent_law,
    apply_identity_law,
    apply_inverse_law,
    distribute_ands,
    distribute_ors,
    coalesce_negations,
    to_cnf,
    to_primitives)

from .utils import ( # noqa
    AbstractTransformationModifier,
    ComposedTransformation,
    ensure_bexpr,
    forever,
    RepeatableAction,
    repeat,
    twice,
    tt_compose)
