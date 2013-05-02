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
__version__ = "0.0b"
#
# This is a library for computing combined dice rolls.
#
# Written by Nicolas Canceill
# Last updated on May 2, 2013
# Hosted at https://github.com/ncanceill/alea_jacta_lib
#

#
#
#
# CLASSES
#

class D:
	def __init__(self,d,n=-1):
		self.d = d
		if n == -1 : n = _nd(self.d)
		self.n = n
	def __add__(self,other):
		return D(_add(self.d,other.d),self.n*other.n)
	def __radd__(self,other):
		return D(_add(other.d,self.d),self.n*other.n)
	def __neg__(self):
		return D(_neg(self.d),self.n)
	def __sub__(self,other):
		return D(_sub(self.d,other.d),self.n*other.n)
	def __rsub__(self,other):
		return D(_sub(other.d,self.d),self.n*other.n)
	def __mul__(self,other):
		return D(_mul(self.d,other.d),self.n*other.n)
	def __rmul__(self,other):
		return D(_mul(other.d,self.d),self.n*other.n)
	def __rpow__(self,other):
		return D(_sml(other,self.d),self.n**other)
	def __str__(self):
		return str_d(self.d,self.n)
	def __repr__(self):
		return repr_d(self.d,self.n)

#
#
#
# FUNCTIONS
#

#
# public

def n(n):
	return D({n:1},1)

def d(n):
	return D(dict((k + 1,1) for k in range(n)))

def q(n):
	return D(dict((k,1) for k in range(n)))

def splfy_frac(x,y):
	def gcd(n,d):
		while d != 0:
			t = d
			d = n%d
			n = t
		return n
	g=gcd(x,y)
	x/=g
	y/=g
	return x,y

def str_d(d,n=1):
	return '\n'.join(_itemize(d,n))

def repr_d(d,n=1):
	return repr(_itemize(d,n))

#
# private

def _itemize(d,n=1):
	return ['{}: {} / {}'.format(k,*splfy_frac(v,n)) for k,v in sorted(d.iteritems())]

def _nd(d):
	n = 0
	for v in d.values():
		n += v
	return n

def _add(dx,dy):
	r = defaultdict(int)
	for x in dx:
		for y in dy:
			r[x + y] += dx[x] * dy[y]
	return r

def _shf(n,d):
	return dict((k,n * v) for k,v in d.iteritems())

def _neg(d):
	return dict((-k,v) for k,v in d.iteritems())

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
