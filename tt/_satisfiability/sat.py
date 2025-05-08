from typing import TYPE_CHECKING, Iterator

from tt.trees import UnaryOperatorExpressionTreeNode

from z3 import Solver, Bool, Not, And, Or, sat

if TYPE_CHECKING:
    from tt.expressions import BooleanExpression


def _z3_all_smt(solver: Solver, initial_terms):
    # See: https://stackoverflow.com/a/70656700

    def block_term(solver: Solver, m, t):
        solver.add(t != m.eval(t, model_completion=True))

    def fix_term(solver: Solver, m, t):
        solver.add(t == m.eval(t, model_completion=True))

    def all_smt_rec(terms):
        if sat == solver.check():
            m = solver.model()
            yield m
            for i in range(len(terms)):
                solver.push()
                block_term(solver, m, terms[i])
                for j in range(i):
                    fix_term(solver, m, terms[j])
                yield from all_smt_rec(terms[i:])
                solver.pop()

    yield from all_smt_rec(list(initial_terms))


def _z3_model_to_result_dict(model, symbol_map):
    result_dict = {}
    for symbol_name, symbol in symbol_map.items():
        solved_value = model.eval(symbol, model_completion=True)
        solved_value = solved_value.py_value()

        result_dict[symbol_name] = int(solved_value)

    return result_dict


def _bexpr_to_z3_solver(bexpr: "BooleanExpression") -> tuple[Solver, dict[str, Bool]]:
    z3_symbol_map = {}
    cnf_tree = bexpr.tree if bexpr.is_cnf else bexpr.tree.to_cnf()

    cnf_clauses = []

    # Define the set of z3 variables based on the CNF form of the
    # expression.
    for clause_root in cnf_tree.iter_cnf_clauses():
        dnf_clauses = []

        for node in clause_root.iter_dnf_clauses():
            is_negated = isinstance(node, UnaryOperatorExpressionTreeNode)
            symbol_str = node.l_child.symbol_name if is_negated else node.symbol_name

            if symbol_str == "0":
                if is_negated:
                    dnf_clauses.append(True)
                else:
                    dnf_clauses.append(False)
            elif symbol_str == "1":
                if is_negated:
                    dnf_clauses.append(False)
                else:
                    dnf_clauses.append(True)
            else:
                z3_symbol = z3_symbol_map.get(symbol_str, None)
                if z3_symbol is None:
                    z3_symbol = Bool(symbol_str)
                    z3_symbol_map[symbol_str] = z3_symbol

                if is_negated:
                    dnf_clauses.append(Not(z3_symbol))
                else:
                    dnf_clauses.append(z3_symbol)

        # Create a z3 representation of this DNF clause.
        cnf_clauses.append(Or(*dnf_clauses))

    # Stitch together the CNF clauses with Boolean ANDs.
    z3_expr = And(*cnf_clauses)

    solver = Solver()
    solver.add(z3_expr)

    # Add assumptions as constrained values.
    for symbol_str, assumed_val in bexpr._constraints.items():
        z3_symbol = z3_symbol_map.get(symbol_str, None)
        if z3_symbol is None:
            # A constraint that doesn't actually appear in the expression.
            continue

        solver.add(z3_symbol == bool(assumed_val))

    return solver, z3_symbol_map


def z3_sat_one(bexpr: "BooleanExpression") -> dict[str, bool] | None:
    solver, symbol_map = _bexpr_to_z3_solver(bexpr)

    if solver.check() == sat:
        model = solver.model()
        return _z3_model_to_result_dict(model, symbol_map)
    else:
        return None


def z3_sat_all(bexpr: "BooleanExpression") -> Iterator[dict[str, bool] | None]:
    solver, symbol_map = _bexpr_to_z3_solver(bexpr)
    for model in _z3_all_smt(solver, list(symbol_map.values())):
        yield _z3_model_to_result_dict(model, symbol_map)
