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

NAME=alea_jacta_lib
VERSION=0.0b

#
# Extensions

PY=.py
PYC=.pyc
TGZ=.tgz

#
# Tools and flags

RM_BIN=rm
RM_FLAGS=-rf
RM=$(RM_BIN) $(RM_FLAGS)

TAR_BIN=tar
TAR_FLAGS=-acvzf
TAR=$(TAR_BIN) $(TAR_FLAGS)

PYTHON=python

#
# Names

PLY_DIR=ply/
DEP=$(PLY_DIR)*$(PY)

SRC_LIB=alea_jacta_lib$(PY)
SRC_CLI=alea_jacta_est$(PY)
SRC=$(SRC_LIB) $(SRC_CLI)

UTL=Makefile README.md

REQ=$(DEP) $(SRC)
REQ=$(DEP) $(SRC)

BC_SRC=$(SRC:$(PY)=$(PYC))
BC_DEP=$(DEP:$(PY)=$(PYC))
BC_REQ=$(REQ:$(PY)=$(PYC))

TMP_PARSER=parse*
TMP=$(TMP_PARSER)

#
#
#
# Targets
#

#
# Package

pkg: $(REQ) clean-all
	$(TAR) $(NAME)-$(VERSION)$(TGZ) $(REQ) $(UTL)

pkg-nodep: $(SRC) clean
	$(TAR) $(NAME)-$(VERSION)-nodep$(TGZ) $(SRC) $(UTL)

#
# Clean

clean:
	$(RM) $(BC_SRC)

clean-dep:
	$(RM) $(BC_DEP)

clean-all:# clean clean-dep
	$(RM) $(BC_REQ)

clean-tmp:
	$(RM) $(TMP)

clean-pkg:
	$(RM) $(NAME)-$(VERSION)$(TGZ)

clean-pkg-nodep:
	$(RM) $(NAME)-$(VERSION)-nodep$(TGZ)

clean-pkg-all:# clean-pkg clean-pkg-nodep
	$(RM) $(NAME)-*$(TGZ)

very-clean: clean-all clean-tmp clean-pkg-all
