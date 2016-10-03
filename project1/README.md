# cis515

## Video

[link to video]

## Requirements

* python 2.7/3.5
* numpy, scipy, matplotlib

## How to run the code
### General Key-bindings

* `t` - toggle marker of curve
* `r` - reset plot

### Problem 1:

Run `p1.py` by
```
python p1.py
```

Press `space` key to end the spline after you have 5 or more deboor control points.

### Problem 2:

Run `p2.py` by
```
python p2.py
```
to plot Bezier curve in 2d.

Run `p2_3d.py` by
```
python p2_3d.py
```
to plot Bezier curve in 3d. After click a point, hold and drag the mouse around, you will see a circle. The radius of the circle will be the `z` coordinate of this control point.


### Implementation details
All methods related to Bezier curves are in module `bezier.py`. 

We implemented 3 different classes for generating Bezier curve.
They are 
* `BezierBernstein`
* `BezierDeCasteljau`
* `BezierSubdivision`


Methods related to interactive plotting are in module `bezier_builder.py`
They are
* `BezierBuilder2D`
* `BezierBuilder3D`



