#
#
# Makefile for alea_jacta_lib v0.0b
#
# Written by Nicolas Canceill.
#

#
#
#
# Variables
#

#
# Extensions

PY=.py
PYC=.pyc

#
# Tools and flags

TAR=tar
TAR_FLAGS=-avzf

PYTHON=python

#
# Names

PLY_DIR=ply/

TMP_PARSER=parse*
TMP= $(TMP_PARSER)

#
#
#
# Targets
#

#
# Clean

clean:
	rm -rf *$(PYC)

very-clean: clean
	rm -rf $(TMP) $(PLY_DIR)*$(PYC)
