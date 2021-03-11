#!/usr/bin/env python3

'''
This is the command line interface for TruSD. As such, this module is only meant
for use from the command line. For information about TruSD, please refer to
help(trusd) or https://github.com/mathiasbockwoldt/TruSD .
'''

import argparse
import sys

import numpy as np
import trusd


def parse_string_as_list(string, func, name, expected_length=0):
	'''
	Split a string by comma (,) and apply a function on each value. The function
	is usually int or float to turn the values into numbers.

	@param string: The string to parse
	@param func: Function to apply on each value of the list
	@param name: The name to report in case of an error
	@param expected_length: Expected length (as integer) of the resulting list
	@returns: A list with the values defined by the parameters
	'''

	lst = string.split(',')

	if expected_length and len(lst) != expected_length:
		print(
			'Input {} has only {} elements, but should have {}.'.format(
				name, len(lst), expected_length
			), file=sys.stderr)
		sys.exit(1)

	try:
		lst = [func(x) for x in lst]
	except ValueError:
		print(
			'Elements in input {} must be of type {}'.format(
				name, func.__name__
			), file=sys.stderr)
		sys.exit(1)

	return lst


def main():
	'''
	Main function for the command line interface. Parse the command line arguments
	and read a file, calculate the likelihoods in a grid and save the results to
	another file.
	'''

	parser = argparse.ArgumentParser(description='''
		TruSD co-infers selection coefficients and genetic drift from allele
		trajectories using a maximum-likelihood framework.''')
	parser.add_argument('infile', metavar='file.txt',
						help='input file name')

	parser.add_argument('-d', '--delimiter', metavar='x', default=',',
						help='''delimiter for input file. Use "tab" or "space"
						for these special characters. [default: %(default)s]''')

	parser.add_argument('-c', '--colskip', metavar='n', default=0, type=int,
						help='''number of columns to skip from the beginning
						(left) [default: %(default)s]''')

	parser.add_argument('-o', '--outfile', metavar='out.csv', default='outfile.csv',
						help='output file [default: %(default)s]')

	parser.add_argument('-n', '--noinfo', action='store_true',
						help='''if set, no informational json file will be
						written along with the result table.''')

	parser.add_argument('-g', '--genepop', metavar='int', default=200, type=int,
						help='population size [default: %(default)s]')

	parser.add_argument('-p', '--proportion', metavar='start,stop,step',
						default='0,1,0.005',
						help='''proportion; give in the form start,stop,step
						without whitespace, where the values are integers or
						floats. Mutually exclusive with -P/--proplist.
						[default: %(default)s]''')

	parser.add_argument('-P', '--proplist', metavar='p1,p2,...', default=None,
						help='''list of proportions; give in the form
						p1,p2,p3,... without whitespace, where px are integers
						or floats. Mutually exclusive with -p/--proportion.
						[default: %(default)s]''')

	parser.add_argument('-s', '--selection', metavar='start,stop,step',
						default='-0.08,0.08,0.002',
						help='''selection coefficient; give in the form
						start,stop,step without whitespace, where the values are
						integers or floats. Mutually exclusive with
						-S/--seleclist. [default: %(default)s]''')

	parser.add_argument('-S', '--seleclist', metavar='s1,s2,...', default=None,
						help='''list of selection coefficients; give in the form
						s1,s2,s3,... without whitespace, where sx are integers
						or floats. Mutually exclusive with -s/--selection.
						[default: %(default)s]''')

	parser.add_argument('-t', '--times', metavar='t1,t2,...', default='0,50',
						help='''time stemps; give in the form t1,t2,t3,...
						without whitespace, where tx are integers.
						[default: %(default)s]''')

	args = parser.parse_args()

	if args.proportion:
		prop = parse_string_as_list(args.proportion, float, '--proportion', 3)
		prop_list = np.arange(prop[0], prop[1] + prop[2], prop[2])
	elif args.proplist:
		prop_list = np.array(
			parse_string_as_list(args.proplist, float, '--proplist')
		)

	if args.selection:
		selec = parse_string_as_list(args.selection, float, '--selection', 3)
		selec_list = np.arange(selec[0], selec[1] + selec[2], selec[2])
	elif args.seleclist:
		selec_list = np.array(
			parse_string_as_list(args.seleclist, float, '--seleclist')
		)

	times = parse_string_as_list(args.times, int, '--times')

	if args.delimiter == 'tab':
		args.delimiter = '\t'
	elif args.delimiter == 'space':
		args.delimiter = ' '

	trajectories = trusd.read_trajectory_file(
		args.infile,
		delimiter=args.delimiter,
		skip_columns=args.colskip
	)

	results = trusd.likelihood_grid(
		trajectories,
		args.genepop,
		prop_list,
		selec_list,
		times
	)

	np.savetxt(args.outfile, results, delimiter=',')

	if not args.noinfo:
		trusd.write_info_file(
			input_file = args.infile,
			output_file = args.outfile,
			command = ' '.join(sys.argv),
			pop_size = args.genepop,
			times = times,
			proportions = list(prop_list),
			selection_coefficients = list(selec_list)
		)
