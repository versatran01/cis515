import unittest
import numpy as np
import numpy.testing as nt
from project3.ge import ge_solve, rand_square
from functools import partial


class TestSolve(unittest.TestCase):
    def setUp(self):
        self.n_max = 5
        self.n_times = 5
        self.n_X = 5

    def random_solve(self, solve_fun, gen_matrix):
        """
        Helper function to randomly generate linear system and test results
        :param solve_fun: function that solves a linear system
        :param gen_matrix: generates A
        :return:
        """
        for i in range(self.n_max):
            n = 2 ** i
            for j in range(self.n_times):
                A = gen_matrix(n)
                for k in range(self.n_X):
                    X = np.random.random((n, k))
                    B = np.dot(A, X)

                    X_sol = solve_fun(A, B)
                    nt.assert_array_almost_equal(X, X_sol)


class TestGe(TestSolve):
    def test_ge_solve_random(self):
        solve_fun = partial(ge_solve, use_scipy=False)
        self.random_solve(solve_fun, rand_square)

    def test_ge_solve_scipy_random(self):
        solve_fun = partial(ge_solve, use_scipy=True)
        self.random_solve(solve_fun, rand_square)
