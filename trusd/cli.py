#!/usr/bin/env python3

import argparse
import trusd


def parse_string_as_list(s, func, name, expected_length=0):
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
	parser = argparse.ArgumentParser(description='TruSD co-infers selection coefficients and genetic drift from allele trajectories using a maximum-likelihood framework.')
	parser.add_argument('infile', metavar='file.txt',
						help='input file name')
	parser.add_argument('-o', '--outfile', metavar='outfile.csv', default='outfile.csv',
						help='output file [default: %(default)s]')
	parser.add_argument('-g', '--genepop', metavar='int', default=200, type=int,
						help='population size [default: %(default)s]')
	parser.add_argument('-p', '--proportion', metavar='start,stop,step', default='0,1,0.005',
						help='proportion; give in the form start,stop,step without whitespace, where the values are integers or floats. [default: %(default)s]')
	parser.add_argument('-s', '--selection', metavar='start,stop,step', default='-0.08,0.08,0.002',
						help='selection coefficient; give in the form start,stop,step without whitespace, where the values are integers or floats. [default: %(default)s]')
	parser.add_argument('-t', '--times', metavar='t1,t2,...', default='0,50',
						help='time stemps; give in the form t1,t2,t3,... without whitespace, where t1 etc. are integers. [default: %(default)s]')

	args = parser.parse_args()

	args.proportion = parse_string_as_list(args.proportion, float, '--proportion', 3)
	args.selection = parse_string_as_list(args.selection, float, '--selection', 3)
	args.times = parse_string_as_list(args.times, int, '--times')

	trusd.infer(args.infile, args.outfile, args.genepop, args.proportion, args.selection, args.times)
