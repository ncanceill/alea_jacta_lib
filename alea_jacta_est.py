#!/usr/bin/python
import sys
import optparse
import logging
import threading
import Queue
from alea_jacta_lib import n,d,q
from alea_jacta_lib import splfy_frac

#
#
#
# ALEA JACTA EST
#

#
# DISCLAIMER: This software is provided for free, with full copyrights, and without any warranty.
#

#
# alea_jacta_est.py
__version__ = "0.0b"
#
# This is a CLI front-end for alea_jacta_lib.
#
# Written by Nicolas Canceill
# Last updated on May 2, 2013
# Hosted at https://github.com/ncanceill/alea_jacta_lib
#

#
#
#
# VARIABLES
#

#
# config

DEBUG = False
VERBOSE = 0

#
# messages

MSG_USAGE = '''
%prog [-d[v|q]] [-o out_type [-w width]] expr0 [expr1 [expr2 ...]]
SYNTAX:
	OPERATORS:	(by precedence)
		x+y		== add numbers or scores x and y
		x-y		== subsctract numbers or scores y from x
		x*y		== multiply numbers or scores x and y
		dy		== the score of 1 dice with 1..y faces
		qy		== the score of 1 dice with 0..y-1 faces
		xdy		== the score of x dices with 1..y faces each
		xqy		== the score of x dices with 0..y-1 faces each
		ny		== the number y
	EXAMPLES:
		1d6				== 1 dice with 6 faces
		3d6				== 3 dices with 6 faces each
		1d4+n5			== 1 dice with 4 faces, plus 5
		n10*1q10+1q10	== Warhammer-like 100dice
 '''
MSG_VERSION = "This is %prog v" + __version__ + " "

MSG_ERROR_OPTION_REQUIRED = "Please provide all required options. "
MSG_ERROR_OPTION_INVALID = "Please provide valid values for options. "

#
#
#
# CLASSES
#

class Computer(threading.Thread):
	def __init__(self,e,q):
		threading.Thread.__init__(self)
		self.expr = e
		self.queue = q
		self._stop = threading.Event()

	def stop(self):
		self._stop.set()

	def stopped(self):
			return self._stop.isSet()

	def run(self):
		self.queue.put((self.expr,yacc.parse(self.expr)))

#
#
#
# FUNCTIONS
#

#
# config tools

def error_option_required(parser,option):
	print_error_option_required(parser,option)
	sys.exit(2)# TODO: stop all threads?

def error_option_invalid(parser,option,value):
	print_error_option_invalid(parser,option,value)
	sys.exit(2)# TODO: stop all threads?

def error_expression_invalid(parser,expression,error):
	print_error_expression_invalid(parser,expression,error)
	sys.exit(1)# TODO: stop all threads?

#
# ply parsing tools (from ply readme example)

import ply.lex as lex

tokens = ('N','D','Q','PLUS','MINUS','TIMES','LPAREN','RPAREN','NUMBER',)
t_N = r'n'
t_D = r'd'
t_Q = r'q'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
def t_NUMBER(t):
	r'\d+'
	try:
		t.value = int(t.value)
	except ValueError:
		print("Integer value too large %d", t.value)
		t.value = 0
	return t
t_ignore = " \t"

def t_newline(t):
	r'\n+'
	t.lexer.lineno += t.value.count("\n")
def t_error(t):
	print("Illegal character '%s'" % t.value[0])
	t.lexer.skip(1)

lex.lex()

import ply.yacc as yacc

precedence = (('left','PLUS'),('left','MINUS'),('left','TIMES'),('right','UMINUS'),('right','UD','UQ'),('right','D','Q'),('right','N'),)

def p_statement_expr(t):
	'statement : expression'
	t[0] = t[1]
def p_expression_binop(t):
	'''expression : expression PLUS expression
		| expression TIMES expression
		| expression MINUS expression
		| NUMBER D NUMBER
		| NUMBER Q NUMBER'''
	if t[2] == '+'  : t[0] = t[1] + t[3]
	elif t[2] == '-'  : t[0] = t[1] - t[3]
	elif t[2] == '*': t[0] = t[1] * t[3]
	elif t[2] == 'd': t[0] = t[1] ** d(t[3])
	elif t[2] == 'q': t[0] = t[1] ** q(t[3])
def p_expression_n(t):
	'expression : N NUMBER'
	t[0] = n(t[2])
def p_expression_ud(t):
	'expression : D NUMBER %prec UD'
	t[0] = d(t[2])
def p_expression_uq(t):
	'expression : Q NUMBER %prec UQ'
	t[0] = q(t[2])
def p_expression_uminus(t):
	'expression : MINUS NUMBER %prec UMINUS'
	t[0] = -t[2]
def p_expression_group(t):
	'expression : LPAREN expression RPAREN'
	t[0] = t[2]
def p_expression_number(t):
	'expression : NUMBER'
	t[0] = t[1]

def p_error(t):
	print("Syntax error at '%s'" % t.value)

yacc.yacc()

#
# output tools

def _indent(indent):
	return indent * ' ' + '\t'

def _inlprint_d(d,indent,probs=True):
	if probs:
		return _indent(indent).join('{}: {}/{}'.format(k,*splfy_frac(v,d.n)) for k,v in sorted(d.d.iteritems()))
	else:
		return _indent(indent).join('{}: {}'.format(k,v) for k,v in sorted(d.d.iteritems()))

def _splprint_d(d,indent,probs=True):
	if probs:
		return '\n'.join('{}:{}{} / {}'.format(k,_indent(indent),*splfy_frac(v,d.n)) for k,v in sorted(d.d.iteritems()))
	else:
		return '\n'.join('{}:{}{}'.format(k,_indent(indent),v) for k,v in sorted(d.d.iteritems()))

def _splplot_d(d,width,indent,probs=True):
	b = min(d.d.itervalues())
	a = width / float(max(d.d.itervalues()) - b + 1)
	if probs:
		return '\n'.join('{0}:{1}{2[0]} / {2[1]}{3}{4}'.format(k,_indent(indent),splfy_frac(v,d.n),_indent(indent),int((v - b) * a + 1) * '#') for k,v in sorted(d.d.iteritems()))
	else:
		return '\n'.join('{}:{}{}{}{}'.format(k,_indent(indent),v,_indent(indent),int((v - b) * a + 1) * '#') for k,v in sorted(d.d.iteritems()))

def print_result(parser,type,expr,d,width,indent,probs=True):
	if VERBOSE >= 0 : print("====================")
	print(expr + '\n')
	if VERBOSE >= 0 and not probs : print "Hits: %d\n" % d.n
	if type == "inline":
		print(_inlprint_d(d,indent,probs))
	elif type == "simple":
		print(_splprint_d(d,indent,probs))
	elif type == "simpleplot":
		print(_splplot_d(d,width,indent,probs))
	else:
		error_option_invalid(parser,"--output",type)
	if VERBOSE >= 0 : print("====================")

#
# logging tools

def print_splash(parser):
	if VERBOSE >= 0 : print("====================")
	parser.print_version()
	if VERBOSE >= 0 : print("====================")

def print_error_option_required(parser,option):
	msg = MSG_ERROR_OPTION_REQUIRED + "Missing: '%s'" % option
	logging.error(msg)
	parser.error(msg)
	parser.print_usage()

def print_error_option_invalid(parser,option,value):
	msg = MSG_ERROR_OPTION_INVALID + "Invalid value '%s' for: '%s'" % (value,option)
	logging.error(msg)
	parser.error(msg)
	parser.print_usage()

#
#
#
# SCRIPT
#

def main():
	# config
	global DEBUG, VERBOSE
	logging.basicConfig(format="%(levelname)s:	%(message)s")
	logging.getLogger().setLevel(logging.ERROR)
	parser = optparse.OptionParser(usage=MSG_USAGE,version=MSG_VERSION)
	group0 = optparse.OptionGroup(parser,"Output options")
	group0.add_option("-o", "--output",dest="output",default="simple",help="output type [%default] ['inline','simple','simpleplot']",metavar="TYPE")
	group0.add_option("-n","--no-probs",action="store_false",dest="probs",default=True,help="disable probability notation")
	group0.add_option("-w", "--width",dest="width",default="64",help="output terminal width [%default]",metavar="TYPE")
	group0.add_option("--indent",dest="indent",default="4",help="output indent size [%default]",metavar="TYPE")
	group1 = optparse.OptionGroup(parser,"Logging options")
	group1.add_option("-d","--debug",action="store_true",dest="debug",default=False,help="enable debug output [%default]")
	group1.add_option("-v","--verbose",action="store_true",dest="verbose",default=False,help="enable verbose output [%default]")
	group1.add_option("-q","--quiet",action="store_true",dest="quiet",default=False,help="enable quiet output [%default]")
	parser.add_option_group(group0)
	parser.add_option_group(group1)
	# options
	(options,args) = parser.parse_args()
	if options.debug:
		logging.getLogger().setLevel(logging.DEBUG)
		DEBUG = True
	if options.verbose:
		logging.getLogger().setLevel(logging.INFO)
		VERBOSE = 1
	if options.verbose:
		logging.getLogger().setLevel(logging.CRITICAL)
		VERBOSE = -1
	if options.output not in ['inline','simple','simpleplot']:
		error_option_invalid(parser,"--output",type)
	options.width = int(options.width)
	options.indent = int(options.indent)
	# launch
	print_splash(parser)
	pool = []
	queue = Queue.Queue()
	result = []
	for expr in args:
		pool.append(Computer(expr,queue))
	# compute
	for t in pool:
		t.start()
	for t in pool:
		result.append(queue.get())
	# results
	for (expr,d) in result:
		print_result(parser,options.output,expr,d,options.width,options.indent,options.probs)

main()
