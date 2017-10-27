"""Interfaces for transforming representations of expressions."""

from .bexpr import (  # noqa
    apply_de_morgans,
    apply_identity_law,
    distribute_ands,
    distribute_ors,
    coalesce_negations,
    to_cnf,
    to_primitives)
