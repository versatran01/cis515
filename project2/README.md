# CIS515 Project 1

## Names

* Chao Qu
* Casey Kent
* Xilei Kuang

## Requirements

* Ubuntu 12.04+
* python 2.7/3.5
* numpy, scipy, matplotlib

## Instructions

`data` folder contains all necessary audio and visual data from `MATLAB`.

`scripts` folder contains all scripts that generates answers or plots for each of the problems.

`tests` folder contains unittests for all the functions implemented for this project. Test coverage is 100%.

`haar.py` contains all functions related to Haar transformation and reconstruction of 1-d vector. Both steps and normalize are implemented in the `haar_step` and `haar_inv_step` functions. The rest functions are calling those internally.

`haar_2d.py` contains all functions reltaed to Haar transformation and reconstruction of 2-d matrix. It depends on functions in `haar.py`.
