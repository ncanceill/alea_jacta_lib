# alea_jacta_lib

A library and CLI for computing combined dice rolls.

## Library

### Basic usage

To use the library:

````python
>>> from alea_jacta_lib import n,d,q
````

Use `n` for numbers (fixed dices), and `d` or `q` for dices.

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
