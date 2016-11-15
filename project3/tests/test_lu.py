from project3.tests.test_ge import TestSolve
from project3.lu import lu_solve_scipy, lu_solve, rand_tridiag
from project3.ge import rand_square
from functools import partial


class TestLu(TestSolve):
    def test_lu_solve_tridiag_random(self):
        f = partial(lu_solve, tridiag=True)
        self.random_solve(f, rand_tridiag)

    def test_lu_solve_scipy_random(self):
        f = partial(lu_solve_scipy, tridiag=False)
        self.random_solve(f, rand_square)

    def test_lu_solve_scipy_tridiag_random(self):
        f = partial(lu_solve_scipy, tridiag=True)
        self.random_solve(f, rand_tridiag)
