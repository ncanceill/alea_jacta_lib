# alea_jacta_lib

A Python 2 library and CLI for computing combined dice rolls.

## Getting started

Please visit the [wiki](../../wiki).

### Requirements

Requires a basic [Python](http://www.python.org) 2 (tested on 2.7.4, should be retro-compatible down to 2.4) installation.

The CLI depends on [PLY](http://www.dabeaz.com/ply) for parsing. PLY is included since version 0.0gamma.

### Setup

You can find the latest version packaged on the [tags page](../../tags). The current version is 0.0gamma: [tgz](../../archive/v0.0c.tar.gz) — [zip](../../archive/v0.0c.zip).

Alternatively, you can clone the repository:

````bash
git clone https://github.com/ncanceill/alea_jacta_lib.git
````

## Basic usage

Start with `./alea_jacta_est.py -h` to get some help (win***s users, use `python.exe -i alea_jacta_est.py`). See the [CLI wiki](../../wiki/CLI) to get some more help.

To use the library directly:

````python
from alea_jacta_lib import n,d,q
````

See the [library wiki](../../wiki/Library) to get help about the library.

## Changelog

### version 0.0rc0

* Refactored code
* Improved parsing (distinction number/dice)
* Improved logging and verbosity management
* Improved display of probabilities (fractions/count)
* Bug fixes (CLI used to trigger library errors)

### version 0.0c

* Refactored code
* Improved Makefile support

## Distribution and contribution

This ReadMe, the library and CLI, and the documentation, distribute under public license.

Any contributions are welcome. Do not hesitate to [drop an issue](../../issues/new) if you found a bug, if you either want to see a new feature or to suggest an improvement, or if you simply have a question.

Copyright (c) 2013 Nicolas Canceill
