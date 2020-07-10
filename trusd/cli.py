#!/usr/bin/env python3

import sys
import argparse
import numpy as np
import trusd


def parse_string_as_list(s, func, name, expected_length=0):
	'''
	Split a string by comma (,) and apply a function on each value. The function
	is usually int or float to turn the values into numbers.

	@param s: The string to parse
	@param func: Function to apply on each value of the list
	@param name: The name to report in case of an error
	@param expected_length: Expected length (as integer) of the resulting list
	@returns: A list with the values defined by the parameters
	'''

	lst = s.split(',')

	if expected_length and len(lst) != expected_length:
		print('Input {} has only {} elements, but should have {}.'.format(name, len(lst), expected_length), file=sys.stderr)
		sys.exit(1)

	try:
		lst = [func(x) for x in lst]
	except ValueError:
		print('Elements in input {} must be of type {}'.format(name, func.__name__), file=sys.stderr)
		sys.exit(1)

	return lst


def main():
	'''
	Main function for the command line interface. Parse the command line arguments
	and read a file, calculate the likelihoods in a grid and save the results to
	another file.
	'''

	parser = argparse.ArgumentParser(description='TruSD co-infers selection coefficients and genetic drift from allele trajectories using a maximum-likelihood framework.')
	parser.add_argument('infile', metavar='file.txt',
						help='input file name')
	parser.add_argument('-o', '--outfile', metavar='outfile.csv', default='outfile.csv',
						help='output file [default: %(default)s]')
	parser.add_argument('-g', '--genepop', metavar='int', default=200, type=int,
						help='population size [default: %(default)s]')
	parser.add_argument('-p', '--proportion', metavar='start,stop,step', default=None,
						help='proportion; give in the form start,stop,step without whitespace, where the values are integers or floats. Mutually exclusive with -P/--proplist.')
	parser.add_argument('-P', '--proplist', metavar='p1,p2,...', default=None,
						help='list of proportions; give in the form p1,p2,p3,... without whitespace, where px are integers or floats. Mutually exclusive with -p/--proportion.')
	parser.add_argument('-s', '--selection', metavar='start,stop,step', default='-0.08,0.08,0.002',
						help='selection coefficient; give in the form start,stop,step without whitespace, where the values are integers or floats. Mutually exclusive with -S/--seleclist.')
	parser.add_argument('-S', '--seleclist', metavar='s1,s2,...', default=None,
						help='list of selection coefficients; give in the form s1,s2,s3,... without whitespace, where sx are integers or floats. Mutually exclusive with -S/--sellist-')
	parser.add_argument('-t', '--times', metavar='t1,t2,...', default='0,50',
						help='time stemps; give in the form t1,t2,t3,... without whitespace, where tx are integers. [default: %(default)s]')

	args = parser.parse_args()

	if args.proportion:
		prop = parse_string_as_list(args.proportion, float, '--proportion', 3)
		prop_list = np.arange(prop[0], prop[1] + prop[2], prop[2])
	elif args.proplist:
		prop_list = np.array(parse_string_as_list(args.proplist, float, '--proplist'))
	else:
		print('Neither -p nor -P were given. Using default value -p 0,1,0.005', file=sys.stderr)
		prop_list = np.arange(0, 1.005, 0.005)

	if args.selection:
		selec = parse_string_as_list(args.selection, float, '--selection', 3)
		selec_list = np.arange(selec[0], selec[1] + selec[2], selec[2])
	elif args.seleclist:
		selec_list = np.array(parse_string_as_list(args.seleclist, float, '--seleclist'))
	else:
		print('Neither -s nor -S were given. Using default value -s -0.08,0.08,0.002', file=sys.stderr)
		selec_list = np.arange(-0.08, 0.082, 0.002)

	times = parse_string_as_list(args.times, int, '--times')

	trajectories = np.loadtxt(infile, delimiter=',', skiprows=1, dtype='uint16')
	results = trusd.likelihood_grid(trajectories, args.genepop, prop_list, selec_list, times)
	np.savetxt(outfile, results, delimiter=',')
