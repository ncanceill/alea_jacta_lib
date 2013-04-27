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
_VERSION = "0.0b"
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
	def __add__(self,other):
		return D(_add(self.d,other.d))
	def __radd__(self,other):
		return D(_add(other.d,self.d))
	def __neg__(self):
		return D(_neg(self.d))
	def __sub__(self,other):
		return D(_sub(self.d,other.d))
	def __rsub__(self,other):
		return D(_sub(other.d,self.d))
	def __mul__(self,other):
		return D(_mul(self.d,other.d))
	def __rmul__(self,other):
		return D(_mul(other.d,self.d))
	def __rpow__(self,other):
		return D(_sml(other,self.d))
	def __str__(self):
		return _str_d(self.d)
	def __repr__(self):
		return _repr_d(self.d)

#
#
#
# FUNCTIONS
#

#
# public

def n(n):
	return D({n:1})

def d(n):
	return D(dict([(k + 1,1) for k in range(n)]))

def q(n):
	return D(dict([(k,1) for k in range(n)]))

#
# private

def _add(dx,dy):
	r = defaultdict(int)
	for x in dx:
		for y in dy:
			r[x + y] += dx[x] * dy[y]
	return r

def _shf(n,d):
	return dict([(k,n * v) for k,v in d.iteritems()])

def _neg(d):
	return dict([(-k,v) for k,v in d.iteritems()])

def _sub(dx,dy):
	r = defaultdict(int)
	for x in dx:
		for y in dy:
			r[x - y] += dx[x] * dy[y]
	return r

def _sum(ds):
	if len(ds) < 2: return ds[0]
	return _add(ds[0],_sum(ds[1:]))

def _sml(n,d):
	return _sum(n*[d])

def _mul(dx,dy):
	r = defaultdict(int)
	for x in dx:
		for y in dy:
			r[x * y] += dx[x] * dy[y]
	return r

def _str_d(d):
	return repr(sorted(dict(d.iteritems())))

def _repr_d(d):
	rep = ""
	for k,v in sorted(d.iteritems()):
		rep += repr((k,v)) + '\n'
	return rep
