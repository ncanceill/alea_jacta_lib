#!/usr/bin/python
from collections import defaultdict

#
#
#
# ALEA JACTA LIB
#

#
# DISCLAIMER: This software is provided for free, with full copyrights, and without any warranty.
#

#
# alea_jacta_lib.py
_VERSION = "0.0a"
#
# This is a library for computing combined dice rolls.
#
# Written by Nicolas Canceill
# Last updated on April 26, 2013
#

#
#
#
# CLASSES
#

class D:
	def __init__(self,d):
		self.d = d
	def __add__(self, other):
		return D(_add(self.d,other.d))
	def __radd__(self, other):
		return D(_add(self.d,other.d))
	def __mul__(self, other):
		return D(_mul(self.d,other.d))
	def __rmul__(self, other):
		return D(_mul(self.d,other.d))
	def __rpow__(self, other):
		return D(_shf(other,self.d))
	def __str__(self):
		return str(self.d)

#
#
#
# FUNCTIONS
#

#
# public

def n(n):
	return D({n:1})

def d(nFaces):
	return D(dict([(score + 1,1) for score in range(nFaces)]))

#
# private

def _add(dx,dy):
	r = defaultdict(int)
	for x in dx:
		for y in dy:
			r[x + y] += dx[x] * dy[y]
	return r

def _shf(n,d):
	return dict([(s,n * o) for s,o in d.iteritems()])

def _sum(ds):
	if len(ds) < 1: return ds[0]
	return _add(ds[0],_sum(ds[1:]))

def _mul(dx,dy):
	r = defaultdict(int)
	for x in dx:
		for y in dy:
			r[x * y] += dx[x] * dy[y]
	return r
