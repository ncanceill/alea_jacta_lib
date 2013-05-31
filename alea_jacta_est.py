#!/usr/bin/python
import sys
import optparse
import logging
import threading
import Queue
from alea_jacta_lib import n,d,q

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
__version__ = "0.0c"
#
# This is a CLI front-end for alea_jacta_lib.
#
# Written by Nicolas Canceill
# Last updated on May 3, 2013
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
# threading

SUCCEED = 0
FAIL = 0
ABORT = 0

#
# messages

MSG_VERSION = "This is %prog v" + __version__ + " "
MSG_USAGE = " [-o <out_type> [-t <indent> -w <width>]] <expr0> [<expr1> ...]]"
MSG_DESC = "A Python 2 library and CLI for computing combined dice rolls."
MSG_EPILOG = "Written by Nicolas Canceill. Hosted at https://github.com/ncanceill/alea_jacta_lib"
MSG_USAGE_LONG = "alea_jacta_est.py" + MSG_USAGE + '''

	''' + MSG_DESC + ''''

		Syntax:

		Operators:	(by precedence)
		x+y		== add numbers or scores x and y
		x-y		== subsctract numbers or scores y from x
		x*y		== multiply numbers or scores x and y
		dy		== the score of 1 dice with 1..y faces
		qy		== the score of 1 dice with 0..y-1 faces
		xdy		== the score of x dices with 1..y faces each
		xqy		== the score of x dices with 0..y-1 faces each
		ny		== the number y

		Examples:
		1d6		== 1 dice with 6 faces
		3d6		== 3 dices with 6 faces each
		1d4+n5		== 1 dice with 4 faces, plus 5
		n10*1q10+1q10	== Warhammer-like 100dice

		''' + MSG_EPILOG

MSG_ERROR_OPTION_REQUIRED = "Please provide all required options. "
MSG_ERROR_OPTION_INVALID = "Please provide valid values for options. "
MSG_ERROR_EXPRESSION_INVALID = "Please use valid expressions. "
MSG_ERROR_PLY_SYNTAX = "Syntax error! "
MSG_ERROR_PLY_TYPE = "Type error! "
MSG_ERROR_PLY_VALUE = "Value error! "

MSG_WARN_OPTION_CONFLICT = "Options should not conflict. "
MSG_WARN_PLY_CHAR = "Illegal character! "

MSG_INFO_START = "Computation starts. "
MSG_INFO_END = "Computation ends. "

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

	def fail(self):
		global FAIL
		FAIL = FAIL + 1
		print_info_end_failure(threading.currentThread())
		sys.exit(1)

	def abort(self):
		global ABORT
		ABORT = ABORT + 1
		print_info_end_abort(threading.currentThread())
		sys.exit(2)

	def run(self):
		print_info_start_expr(self)
		self.queue.put((self.expr,yacc.parse(self.expr)))
		global SUCCEED
		SUCCEED = SUCCEED + 1
		print_info_end_success(self)

#	def stop(self):
#		self._stop.set()
#	def stopped(self):
#			return self._stop.isSet()

#
#
#
# FUNCTIONS
#

#
# config tools

def error_expression_invalid(error):
	print_error_expression_invalid(threading.currentThread().expr,error)
	threading.currentThread().fail()

def error_option_required(parser,option):
	print_error_option_required(parser,option)
	sys.exit(2)# TODO: stop all threads?
def error_option_invalid(parser,option,value):
	print_error_option_invalid(parser,option,value)
	sys.exit(2)# TODO: stop all threads?

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
	except ValueError as ve:# should never happen
		error_expression_invalid(threading.currentThread().expr,MSG_ERROR_PLY_SYNTAX + "(%s)" % str(ve))
		t.value = 0
	return t
t_ignore = " \t"

def t_newline(t):
	r'\n+'
	t.lexer.lineno += t.value.count("\n")
def t_error(t):
	print_warn_ply_char(t.value[0],skipping=True)
	t.lexer.skip(1)

lex.lex()

import ply.yacc as yacc

precedence = (('left','PLUS'),('left','MINUS'),('left','TIMES'),('right','UMINUS'),('right','UD','UQ'),('right','D','Q'),('right','N'),)

def p_statement_dexpr(t):
	'statement : d_expression'
	t[0] = t[1]
def p_statement_iexpr(t):
	'statement : i_expression'
	t[0] = n(t[1])
def p_d_expression_binop(t):
	'''d_expression : d_expression PLUS d_expression
		| d_expression MINUS d_expression
		| d_expression TIMES d_expression
		| i_expression D i_expression
		| i_expression Q i_expression'''
	try:
		if t[2] == '+'  : t[0] = t[1] + t[3]
		elif t[2] == '-'  : t[0] = t[1] - t[3]
		elif t[2] == '*': t[0] = t[1] * t[3]
		elif t[2] == 'd': t[0] = t[1] ** d(t[3])
		elif t[2] == 'q': t[0] = t[1] ** q(t[3])
	except TypeError as te:
		error_expression_invalid(threading.currentThread().expr,MSG_ERROR_PLY_TYPE + "(%s)" % str(te))
def p_i_expression_binop(t):
	'''i_expression : i_expression PLUS i_expression
		| i_expression MINUS i_expression
		| i_expression TIMES i_expression'''
	try:
		if t[2] == '+'  : t[0] = t[1] + t[3]
		elif t[2] == '-'  : t[0] = t[1] - t[3]
		elif t[2] == '*': t[0] = t[1] * t[3]
	except TypeError as te:
		error_expression_invalid(threading.currentThread().expr,MSG_ERROR_PLY_TYPE + "(%s)" % str(te))
def p_d_expression_binop_lefti(t):
	'''d_expression : i_expression PLUS d_expression
		| i_expression MINUS d_expression
		| i_expression TIMES d_expression'''
	try:
		if t[2] == '+'  : t[0] = n(t[1]) + t[3]
		elif t[2] == '-'  : t[0] = n(t[1]) - t[3]
		elif t[2] == '*': t[0] = n(t[1]) * t[3]
	except TypeError as te:
		error_expression_invalid(threading.currentThread().expr,MSG_ERROR_PLY_TYPE + "(%s)" % str(te))
def p_d_expression_binop_righti(t):
	'''d_expression : d_expression PLUS i_expression
		| d_expression MINUS i_expression
		| d_expression TIMES i_expression'''
	try:
		if t[2] == '+'  : t[0] = t[1] + n(t[3])
		elif t[2] == '-'  : t[0] = t[1] - n(t[3])
		elif t[2] == '*': t[0] = t[1] * n(t[3])
	except TypeError as te:
		error_expression_invalid(threading.currentThread().expr,MSG_ERROR_PLY_TYPE + "(%s)" % str(te))

def p_expression_n(t):
	'd_expression : N i_expression'
	t[0] = n(t[2])
def p_expression_ud(t):
	'd_expression : D i_expression %prec UD'
	t[0] = d(t[2])
def p_expression_uq(t):
	'd_expression : Q i_expression %prec UQ'
	t[0] = q(t[2])
def p_expression_uminus_i(t):
	'i_expression : MINUS i_expression %prec UMINUS'
	t[0] = -t[2]
def p_expression_uminus_d(t):
	'd_expression : MINUS d_expression %prec UMINUS'
	t[0] = -t[2]
def p_expression_group_i(t):
	'i_expression : LPAREN i_expression RPAREN'
	t[0] = t[2]
def p_expression_group_d(t):
	'd_expression : LPAREN d_expression RPAREN'
	t[0] = t[2]
def p_expression_number(t):
	'i_expression : NUMBER'
	t[0] = t[1]

def p_error(t):
	error_expression_invalid(MSG_ERROR_PLY_SYNTAX)

yacc.yacc()

#
# output tools

def gcd(*numbers):
	from fractions import gcd
	return reduce(gcd,numbers)
def lcm(*numbers):
	def lcm(a,b):
		return (a * b) // gcd(a,b)
	return reduce(lcm,numbers)
def _norm_fracs(d):
	denom = lcm(*d.d.itervalues())
	return [(k,'{}/{}'.format(v*denom/d.n,denom),v) for k,v in sorted(d.d.iteritems())]

def _indent(indent):
	return indent * ' ' + '\t'
def _inlprint_d(d,i,probs=True,float_probs=False):
	if probs:
		if float_probs:
			return _indent(i).join('{}: {:.3}'.format(k,v/float(d.n)) for k,v in sorted(d.d.iteritems()))
		return _indent(i).join('{}: {}'.format(k,p) for k,p,v in _norm_fracs(d))
	return _indent(i).join('{}: {}'.format(k,v) for k,v in sorted(d.d.iteritems()))
def _splprint_d(d,i,probs=True,float_probs=False):
	if probs:
		if float_probs:
			return '\n'.join('{}:{}{:.3}'.format(k,_indent(i),v/float(d.n)) for k,v in sorted(d.d.iteritems()))
		return '\n'.join('{}:{}{}'.format(k,_indent(i),p) for k,p,v in _norm_fracs(d))
	return '\n'.join('{}:{}{}'.format(k,_indent(i),v) for k,v in sorted(d.d.iteritems()))
def _splplot_d(d,width,i,probs=True,float_probs=False):
	b = min(d.d.itervalues())
	a = width / float(max(d.d.itervalues()) - b + 1)
	def _splplotline(v):
		return int((v - b) * a + 1) * '#'
	if probs:
		if float_probs:
			return '\n'.join('{}:{}{:.3}{}{}'.format(k,_indent(i),v/float(d.n),_indent(i),_splplotline(v)) for k,v in sorted(d.d.iteritems()))
		return '\n'.join('{}:{}{}{}{}'.format(k,_indent(i),p,_indent(i),_splplotline(v)) for k,p,v in _norm_fracs(d))
	return '\n'.join('{}:{}{}{}{}'.format(k,_indent(i),v,_indent(i),_splplotline(v)) for k,v in sorted(d.d.iteritems()))

def print_result(parser,type,expr,d,width,indent,probs=True,float_probs=False):
	if VERBOSE >= 0 : print("====================")
	print(expr)
	if VERBOSE >= 0 and not probs : print "\nHits: %d\n" % d.n
	if type == "inline":
		print(_inlprint_d(d,indent,probs,float_probs))
	elif type == "simple":
		print(_splprint_d(d,indent,probs,float_probs))
	elif type == "simpleplot":
		print(_splplot_d(d,width,indent,probs,float_probs))
	else:
		error_option_invalid(parser,"--output",type)
	if VERBOSE >= 0 : print("====================")

#
# logging tools

def print_splash(parser):
	if VERBOSE >= 0 : print("====================")
	parser.print_version()
	if VERBOSE >= 0 : print("====================")

def print_usage():
	print "Usage:\t" + MSG_USAGE
def print_usage_long():
	print "Usage:\t" + MSG_USAGE_LONG

def print_error_option_required(parser,option):
	msg = MSG_ERROR_OPTION_REQUIRED + "Missing: '%s'. " % option
	logging.error(msg)
	if VERBOSE >= 1 : parser.error(msg)
def print_error_option_invalid(parser,option,value):
	msg = MSG_ERROR_OPTION_INVALID + "Invalid value '%s' for option '%s'. " % (value,option)
	logging.error(msg)
	if VERBOSE >= 1 : parser.error(msg)
def print_error_expression_invalid(expr,error):
	msg = MSG_ERROR_EXPRESSION_INVALID + "PLY: %s in expression '%s'." % (error,expr)
	logging.error(msg)

def print_warn_option_conflict(parser,opt_x,opt_y):
	msg = MSG_WARN_OPTION_CONFLICT + "'%s' and '%s' are mutually exclusive, ignoring '%s'. " % (opt_x,opt_y,opt_x)
	logging.warning(msg)
def print_warn_ply_char(c,skipping=True):
	msg = MSG_WARN_PLY_CHAR + "Character '%s' is not allowed. " % (c)
	if skipping : msg += "Skip and proceed. "
	logging.warning(msg)

def print_info_start(n):
	msg = MSG_INFO_START + "Threading to evaluate %d expression(s). " % (n)
	logging.info(msg)

def print_info_start_expr(thrd):
	msg = MSG_INFO_START + "Evaluating '%s' in %s. " % (thrd.expr,thrd.name)
	logging.info(msg)

def print_info_end_success(thrd):
	msg = MSG_INFO_END + "Successfully evaluated '%s' in %s. " % (thrd.expr,thrd.name)
	logging.info(msg)

def print_info_end_failure(thrd):
	msg = MSG_INFO_END + "Failed to evaluate '%s' in %s. " % (thrd.expr,thrd.name)
	logging.info(msg)

def print_info_end_abort(thrd):
	msg = MSG_INFO_END + "Aborted evaluation of '%s' in %s. " % (thrd.expr,thrd.name)
	logging.info(msg)

def print_info_end(s,f,a):
	msg = MSG_INFO_END + "All threads dead, %d succeeded, %d failed, %d aborted. " % (s,f,a)
	logging.info(msg)

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
	# options
	parser = optparse.OptionParser(version=MSG_VERSION,usage="%prog" + MSG_USAGE,description=MSG_DESC,epilog=MSG_EPILOG,conflict_handler="error")
	group0 = optparse.OptionGroup(parser,"Output options")
	group0.add_option("-o","--output",dest="output",default="simple",help="output type [%default] ['inline','simple','simpleplot']",metavar="TYPE")
	group0.add_option("-n","--no-probs",action="store_true",dest="no_probs",default=False,help="display probabilities as counts [%default]")
	group0.add_option("-f","--float-probs",action="store_true",dest="float_probs",default=False,help="display probabilites as floats [%default]")
	group0.add_option("-w","--width",dest="width",default="64",help="output terminal width [%default]",metavar="TYPE")
	group0.add_option("-t","--indent",dest="indent",default="8",help="output indent size [%default]",metavar="TYPE")
	group1 = optparse.OptionGroup(parser,"Logging options")
	group1.add_option("-d","--debug",action="store_true",dest="debug",default=False,help="enable debug output [%default]")
	group1.add_option("-v","--verbose",action="store_true",dest="verbose",default=False,help="enable verbose output [%default]")
	group1.add_option("-V","--very-verbose",action="store_true",dest="vverbose",default=False,help="enable very verbose output [%default]")
	group1.add_option("-q","--quiet",action="store_true",dest="quiet",default=False,help="enable quiet output [%default]")
	parser.add_option("-H","--help-syntax",action="store_true",dest="help",default=False,help="show syntax help message and exit")
	parser.add_option_group(group0)
	parser.add_option_group(group1)
	print_splash(parser)
	# command parsing
	(options,args) = parser.parse_args()
	if options.help:
		print_usage_long()
		return
	if options.debug:
		logging.getLogger().setLevel(logging.DEBUG)
		DEBUG = True
	if options.quiet:
		logging.getLogger().setLevel(logging.CRITICAL)
		VERBOSE = -1
	if options.verbose:
		logging.getLogger().setLevel(logging.WARNING)
		VERBOSE = 1
		if options.quiet : print_warn_option_conflict(parser,"-q","-v")
	if options.vverbose:
		logging.getLogger().setLevel(logging.INFO)
		VERBOSE = 2
		if options.verbose : print_warn_option_conflict(parser,"-v","-V")
		if options.quiet : print_warn_option_conflict(parser,"-q","-V")
	if options.output not in ['inline','simple','simpleplot']:
		error_option_invalid(parser,"--output",options.output)
	if options.no_probs and options.float_probs : print_warn_option_conflict(parser,"--float-probs","--no-probs")
	options.width = int(options.width)
	options.indent = int(options.indent)
	# launch
	pool = []
	queue = Queue.Queue()
	result = []
	for expr in args:
		pool.append(Computer(expr,queue))
	# exec
	print_info_start(len(pool))
	for t in pool:
		t.start()
	for t in pool:
		t.join()
	# return
	while not queue.empty():
		result.append(queue.get())
	print_info_end(SUCCEED,FAIL,ABORT)
	for (expr,d) in result:
		print_result(parser,options.output,expr,d,options.width,options.indent,not options.no_probs,options.float_probs)

if __name__ == '__main__':
    main()
