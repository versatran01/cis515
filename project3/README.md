# CIS515 Project 3

## Names

* Chao Qu
* Casey Kent
* Xilei Kuang

## Requirements

* Ubuntu 12.04+
* python 2.7/3.5
* numpy, scipy, matplotlib

## Video

https://youtu.be/bGGjKjAN238

## Instructions

`tests` folder contains unittests for all the functions implemented for this project. Test coverage is 92%.

`scripts` folder contains scripts for generating all plots in the report.

Gaussian elimination with partial pivoting for solving linear systems is implemented in `ge.py` as `ge_solve`, along with `gauss_elim` and `back_sub`.

`ge_solve` optionally takes an argument `use_scipy` to enable fast forward- and back-substitution via `scipy.linalg.solve_triangular`.

LU-decomposition for solving tridiagonal systems is implemented in `lu.py` as `lu_solve_tridiag`. It again take `use_scipy` as an optional argument to enable fast forward- and back-substitution.

A few other methods of solving linear systems are implemented, mostly based on scipy's implementation.
