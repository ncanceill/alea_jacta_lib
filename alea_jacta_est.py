#!/usr/bin/python
import sys
import optparse
import logging
from alea_jacta_lib import *

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
VERSION = "0.0a"
#
# This is a CLI front-end for AleaJactaLib.
#
# Written by Nicolas Canceill
# Last updated on April 26, 2013
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

MSG_USAGE = "%prog [-DV] expr0 [expr1 [expr2 ...]] "
MSG_VERSION = "This is %prog v" + VERSION + " "

MSG_ERROR_OPTION_REQUIRED = "Please provide all required options. "

#
#
#
# FUNCTIONS
#

#
# config tools

def error_option_required(parser,option):
	print_error_option_required(parser,option)
	sys.exit(-1)

#
# logging tools

def print_splash(parser):
	print("====================")
	parser.print_version()
	print("====================")

def print_error_option_required(parser,option):
	parser.error(MSG_ERROR_OPTION_REQUIRED + "Missing: \"" + option + "\"")
	parser.print_usage()

#
#
#
# SCRIPT
#

def main():
	global DEBUG
	logging.basicConfig(format="%(levelname)s:	%(message)s")
	parser = optparse.OptionParser(usage=MSG_USAGE,version=MSG_VERSION)
	group0 = optparse.OptionGroup(parser,"Mandatory options")
	group1 = optparse.OptionGroup(parser,"Additional options")
	group1.add_option("-D","--debug",action="store_true",dest="debug",default=False,help="enable debug output [%default]")
	group1.add_option("-V","--verbose",action="store_true",dest="verbose",default=False,help="enable verbose output [%default]")
	parser.add_option_group(group0)
	parser.add_option_group(group1)
	(options,args) = parser.parse_args()
	if options.debug:
		DEBUG = true
	for expr in args:
