# CIS515 Project 1

## Names

* Chao Qu
* Casey Kent
* Xilei Kuang

## Videos

B-spline and Bezier Curve

https://www.youtube.com/watch?v=Lyj-4JJX70Q

Bezier Curve 3D

https://www.youtube.com/watch?v=pIlueSqXc1k

## Requirements

* Ubuntu 12.04+
* python 2.7/3.5
* numpy, scipy, matplotlib

## Instructions
### General Key-bindings

* `t` - toggle marker of curve
* `r` - reset plot

### Problem 1:

Run `p1.py` by
```
python p1.py
```
This will prompt you with a matplotlib figure and you can then click within the axes area to add deboor control points.

Press `space` key to end the spline after you have 5 or more deboor control points.

### Problem 2:

Run `p2.py` by
```
python p2.py
```
to plot Bezier curve in 2d.

This will prompt you with a matplotlib figure and you can then click within the axes area to add Bezier control points.

Run `p2_3d.py` by
```
python p2_3d.py
```
to plot Bezier curve in 3d.

This will prompt you with a matplotlib figure with two axes. You can then click within the left axes are to add Bezier control points.

After click a point, hold and drag the mouse around, you will see a circle. The radius of the circle will be the `z` coordinate of this control point.

### Implementation Details
All methods related to Bezier curves are in module `bezier.py`.

We implemented 3 different classes for generating Bezier curve.
They are
* `BezierBernstein`
* `BezierDeCasteljau`
* `BezierSubdivision`

All methods related to B-Spline are in module `deboor.py`
They are
* `deboor_to_bezier`
* `deboor_1st`
* `deboor_2nd`
* `deboor_ith`

Methods related to interactive plotting are in module `bezier_builder.py` and `deboor_builder.py`.
They are
* `BezierBuilder2D`
* `BezierBuilder3D`
* `DeboorBuilder2D`

Files in `examples/`, `scripts/`, `tests/` are not used.
