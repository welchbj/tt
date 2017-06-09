"""Tests for the Python wrapper around the PicoSAT C-extension."""

import unittest

from tt.errors import (
    InvalidArgumentTypeError,
    InvalidArgumentValueError)
from tt.satisfiability.picosat import (
    sat_all,
    sat_one,
    VERSION)


class TestPicosat(unittest.TestCase):

    def test_version(self):
        """Test the PicoSAT library version."""
        self.assertEqual(965, VERSION)

    def test_sat_one_single_clause_satisfiable(self):
        """Test a single clause and look for a satisfiable solution."""
        self.assertEqual([1], sat_one([[1]]))

    def test_sat_one_single_clause_assumptions_satisfiable(self):
        """Test a single clause with assumptions, ensuring solution found."""
        self.assertEqual([1, 2, -3, -4],
                         sat_one([[1, 4], [2, 3], [1, -3], [-3]],
                                 assumptions=[-4]))

    def test_sat_one_assumptions_single_clause_not_satisfiable(self):
        """Assert no solution found for an infeasible assumption."""
        self.assertEqual(None, sat_one([[1]], [-1]))
        self.assertEqual(None, sat_one([[-1]], [1]))

    def test_sat_one_multi_clauses_satisfiable(self):
        """Test multi-clause satisfiability with a single solution."""
        self.assertEqual([-1, 2, 3], sat_one([[1, 2, 3], [-1, 2], [3]]))

    def test_sat_one_multi_clauses_not_satisfiable(self):
        """Test multi-clause satisfiability without a solution."""
        self.assertEqual(None, sat_one([[1, 2], [-1, 2], [-2]]))

    def test_sat_one_multi_clauses_assumptions_satisfiable(self):
        """Test multi-clause sat with assumptions with a single solution."""
        self.assertEqual([-1, 2, 3], sat_one([[1, 2, 3], [-1, 2, 3]], [-1]))

    def test_sat_one_multi_clauses_assumptions_not_satisfiable(self):
        """Test multi-clause sat with assumptions without a solution."""
        self.assertEqual(None, sat_one([[-1, -2], [1]], [2]))

    def test_sat_one_assumptions_not_in_clauses(self):
        """Test that assumptions not in clauses are still in the solution."""
        self.assertEqual([1, -2, 3, 4],
                         sat_one([[1, 2], [-2]], assumptions=[3, 4]))

    def test_sat_all_without_assumptions_not_satisfiable(self):
        """Test sat_all w/o assumptions that produces no solutions."""
        count = 0
        for _ in sat_all([[1, 2], [-1, -2], [1], [2]]):
            count += 1
        self.assertEqual(0, count)

    def test_sat_all_without_assumptions_satisfiable_one_sol(self):
        """Test sat_all w/o assumptions that produces a single solution."""
        count = 0
        expected = [-1, -2, 3, 4]
        for solution in sat_all([[1, 2, 3], [-1], [-2], [-3, 4]]):
            self.assertEqual(expected, solution)
            count += 1
        self.assertEqual(1, count)

    def test_sat_all_without_assumptions_satisfiable_multiple_sols(self):
        """Test sat_all w/o assumptions producing multiple solutions."""
        count = 0
        expected = [
            [-1, -2, 3, -4],
            [-1, 2, -3, -4],
            [1, 2, -3, -4],
            [1, -2, -3, -4]]
        for solution in sat_all([[1, 2, 3, 4], [-2, -3], [-4], [-1, -3]]):
            self.assertIn(solution, expected)
            count += 1
        self.assertEqual(4, count)

    def test_sat_all_with_assumptions_not_satisfiable(self):
        """Test sat_all w/ assumptions that produces no solutions."""
        count = 0
        for _ in sat_all([[1, 2, 3], [2, 3], [-1]], assumptions=[-2, -3]):
            count += 1
        self.assertEqual(0, count)

    def test_sat_all_with_assumptions_satisfiable_one_sol(self):
        """Test sat_all w/ assumptions producing a single solution."""
        count = 0
        expected = [-1, 2, -3, -4, 5]
        for solution in sat_all([[1, 2], [2, 3], [3, 4, 5]],
                                assumptions=[-1, -3, -4]):
            self.assertEqual(expected, solution)
            count += 1
        self.assertEqual(1, count)

    def test_sat_all_with_assumptions_satisfiable_multiple_sols(self):
        """Test sat_all w/ assumptions producing multiple solutions."""
        count = 0
        expected = [
            [1, -2, 3, -4, 5],
            [1, -2, 3, -4, -5]]
        for solution in sat_all([[1, 2, 3, 4, 5], [-1, -2], [-3, -4]],
                                assumptions=[1, 3]):
            self.assertIn(solution, expected)
            count += 1
        self.assertEqual(2, count)

    def test_passing_non_list_clauses(self):
        """Test passing a non-list as the clauses argument."""
        with self.assertRaises(InvalidArgumentTypeError):
            sat_one(None)

        with self.assertRaises(InvalidArgumentTypeError):
            sat_all(None)

    def test_passing_non_list_assumptions(self):
        """Test passing an invalid non-list as the assumptions argument."""
        with self.assertRaises(InvalidArgumentTypeError):
            sat_one([[1, 2, 3]], assumptions=float())

        with self.assertRaises(InvalidArgumentTypeError):
            sat_all([[1, 2, 3]], assumptions=float())

    def test_passing_empty_list_clauses(self):
        """Test passing an empty list as clauses causes an error."""
        with self.assertRaises(InvalidArgumentValueError):
            sat_one([])

        with self.assertRaises(InvalidArgumentValueError):
            sat_all([])

    def test_passing_empty_list_assumptions(self):
        """Test passing an empty list as assumptions causes an error."""
        with self.assertRaises(InvalidArgumentValueError):
            sat_one([[1, 2]], assumptions=[])

        with self.assertRaises(InvalidArgumentValueError):
            sat_all([[1, 2]], assumptions=[])

    def test_passing_empty_inner_list_clauses(self):
        """Test an error is raised when passing an empty list of clauses."""
        with self.assertRaises(InvalidArgumentValueError):
            sat_one([[1], [], [2, 3]])

        with self.assertRaises(InvalidArgumentValueError):
            sat_all([[1], [], [2, 3]])

    def test_passing_non_int_inner_list_clauses(self):
        """Test an error is raised when passing a non-int in clauses."""
        with self.assertRaises(InvalidArgumentTypeError):
            sat_one([[1, 2, 3], [-2], ['string']])

        with self.assertRaises(InvalidArgumentTypeError):
            sat_all([[1, 2, 3], [-2], ['string']])

    def test_passing_zeroes_inner_list_clauses(self):
        """Test an error is raised when zeroes are passed in clauses."""
        with self.assertRaises(InvalidArgumentValueError):
            sat_one([[1, 0, 3], [2], [3]])

        with self.assertRaises(InvalidArgumentValueError):
            sat_all([[1, 0, 3], [2], [3]])

    def test_passing_list_of_non_ints_assumptions(self):
        """Test an error is raised when non-ints are passed in assumptions."""
        with self.assertRaises(InvalidArgumentTypeError):
            sat_one([[1, -2], [-1]], assumptions=[1, 'string'])

        with self.assertRaises(InvalidArgumentTypeError):
            sat_all([[1, -2], [-1]], assumptions=[1, 'string'])

    def test_passing_list_containing_zeroes_assumptions(self):
        """Test an error is rasied when zeroes are passed in assumptions."""
        with self.assertRaises(InvalidArgumentValueError):
            sat_one([[1, -2], [-1]], assumptions=[1, 2, 3, 0])

        with self.assertRaises(InvalidArgumentValueError):
            sat_all([[1, -2], [-1]], assumptions=[1, 2, 3, 0])
