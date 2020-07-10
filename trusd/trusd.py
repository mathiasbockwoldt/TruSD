#!/usr/bin/env python3

from functools import lru_cache

import numpy as np
from scipy.special import comb


@lru_cache(maxsize=None)
def wright_fisher_trans_matrix(selection_coefficient, num_generations, genepop):
	'''
	Returns the Wrigth-Fisher transition matrix given the selection coefficient,
	the number of generations and the genetic population.
	'''

	matrix = np.full((genepop + 1, genepop + 1), np.nan, dtype=np.float64)

	for n in range(genepop + 1):
		for m in range(genepop + 1):
			m_over_genepop = m / genepop
			first_product = (m_over_genepop + selection_coefficient * m_over_genepop * (1 - m_over_genepop)) ** n
			second_product = (1 - m_over_genepop - selection_coefficient * m_over_genepop*(1 - m_over_genepop))**(genepop - n)
			matrix[n, m] = comb(genepop, n) * first_product * second_product

	matrix = np.linalg.matrix_power(matrix, num_generations)

	return matrix


def likelihood(selection_coefficient, proportion, time_points, trajectories, genepop):
	result = 0
	for time_index in range(len(time_points) - 1):
		timepoint = time_points[time_index + 1] - time_points[time_index]

		transition_prob_sel = wright_fisher_trans_matrix(selection_coefficient, timepoint, genepop)
		transition_prob_neut = wright_fisher_trans_matrix(0, timepoint, genepop)

		for trajectory in range(len(trajectories)):
			row = trajectories[trajectory, time_index + 1]
			col = trajectories[trajectory, time_index]
			a = transition_prob_sel[row, col]
			b = transition_prob_neut[row, col]
			result += np.log((proportion * a + (1 - proportion) * b))

	return result


def infer(trajectories, genepop, proportions, selections, tvec):
	#creates a grid of parameters
	pseq = np.arange(proportions[0], proportions[1] + proportions[2], proportions[2])
	plen = len(pseq)
	sseq = np.arange(selections[0], selections[1] + selections[2], selections[2])
	slen = len(sseq)

	#calculates the log-likelihood for each point on the grid
	mat = np.full((slen + 0, plen + 0), np.nan, dtype=np.float64)
	for i in range(slen):
		s = sseq[i]
		for j in range(plen):
			p = pseq[j]
			mat[i, j] = likelihood(s, p, tvec, trajectories, genepop)

	return mat


def main(infile, outfile, genepop, proportions, selections, tvec):
	trajectories = np.loadtxt(infile, delimiter=',', skiprows=1, dtype='uint16')

	results = infer(trajectories, genepop, proportions, selections, tvec)

	np.savetxt(outfile, mat, delimiter=',')


if __name__ == '__main__':
	import cli
	cli.main()
