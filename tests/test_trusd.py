#!/usr/bin/env python3

import numpy as np
import trusd


def test_wf_matrix():
	ex_0_0_3 = np.array([[1., 0., 0., 0.],[0., 1., 0., 0.],[0., 0., 1., 0.],[0., 0., 0., 1.]])
	ex_005_5_3 = np.array([[1., 0.57065153, 0.24147056, 0.],[0., 0.06579579, 0.06206989, 0.],[0., 0.06860101, 0.06579337, 0.],[0., 0.29495167, 0.63066619, 1.]])

	assert np.allclose(trusd.wright_fisher_trans_matrix(0, 0, 3), ex_0_0_3)

	assert np.allclose(trusd.wright_fisher_trans_matrix(0.05, 5, 3), ex_005_5_3)


def test_likelihood():
	pass
