from project3.tests.test_ge import TestSolve
from project3.lu import lu_solve_scipy, lu_solve_tridiag, rand_tridiag
from project3.ge import rand_square
from functools import partial


class TestLu(TestSolve):
    def test_lu_solve_tridiag_random(self):
        f = partial(lu_solve_tridiag)
        self.random_solve(f, rand_tridiag)
        g = partial(lu_solve_tridiag, use_scipy=False)
        self.random_solve(g, rand_tridiag)

    def test_lu_solve_scipy_random(self):
        f = partial(lu_solve_scipy)
        self.random_solve(f, rand_square)

        # def test_lu_solve_scipy_tridiag_random(self):
        #     f = partial(lu_solve_scipy, tridiag=True)
        #     self.random_solve(f, rand_tridiag)
