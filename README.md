# alea_jacta_lib

A Python 2 library and CLI for computing combined dice rolls.

## Requirements

Requires a basic Python 2 (tested on 2.7.4, should be retro-compatible down to 2.4) installation.

## Library

### Basic usage

To use the library:

````python
from alea_jacta_lib import n,d,q
````

Use `n` for numbers (fixed dices), and `d` or `q` for dices. While `d(x)` and `q(x)` both refer to dices with _x_ faces, `d` starts at 1 while `q` starts at 0, therefore `d(x) == q(x) + n(1)`.

Dices support inner addition `d(x) + d(y)`, inner substraction `d(x) - d(y)`, unary substraction `-d(x)`, inner multiplication `d(x) * d(y)`, and left outer multiplication `x ** d(y)`.

### Examples

````python
>>> d(6)
>>> n(3)*(2**d(6) + q(4) + n(2))
````

## Command Line Interface

### Basic usage

Start with:

````bash
./alea_jacta_est.py -h
````

### Dependencies

Depends on [PLY](http://www.dabeaz.com/ply) for parsing.

### Examples

````bash
./alea_jacta_est.py 2d6
./alea_jacta_est.py -o simpleplot -w 60 n2*(3q10-1d6)
````
