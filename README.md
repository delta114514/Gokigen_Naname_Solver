# Gokigen_naname_solver

This is a solver of Japanese logic puzzle [Gokigen Naname](https://en.wikipedia.org/wiki/Gokigen_Naname) published by Nikoli.

# Usage
Use `solve` function to find answer. You have to pass a argument `edge` which is 2-dimensional list and length of it and the length of lists in itself are the same, and elements of lists in it shows how many intersections on that grid. if the number of intersections is not specified, use number bigger than 4.

Like below:
```python

>>> from solve import solve, pretty_print

>>> solve.solve([[5, 5, 5, 1, 0], [5, 4, 5, 5, 1], [1, 5, 5, 2, 1], [5, 5, 2, 2, 5], [0, 5, 1, 5, 5]])
[[<Angle.LEFT_UP: 1>, <Angle.RIGHT_UP: 0>, <Angle.LEFT_UP: 1>, <Angle.LEFT_UP: 1>], [<Angle.RIGHT_UP: 0>, <Angle.LEFT_UP: 1>, <Angle.LEFT_UP: 1>, <Angle.LEFT_UP: 1>], [<Angle.RIGHT_UP: 0>, <Angle.LEFT_UP: 1>, <Angle.LEFT_UP: 1>, <Angle.LEFT_UP: 1>], [<Angle.LEFT_UP: 1>, <Angle.LEFT_UP: 1>, <Angle.LEFT_UP: 1>, <Angle.LEFT_UP: 1>]]

>>> pretty_print(_)
---------
|＼／＼＼|
|／＼＼＼|
|／＼＼＼|
|＼＼＼＼|
---------

``` 