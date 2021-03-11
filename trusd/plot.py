#!/usr/bin/env python3

import os
import sys

DISPLAY_PRESENT = 'DISPLAY' in os.environ

if not DISPLAY_PRESENT:
	import matplotlib
	matplotlib.use('agg')

import numpy as np
import matplotlib.pyplot as plt


def contour_plot(input_file, num_trajectories, s_list, p_list, s_value, p_value,
				contour_line_subtract, delimiter=',', save=True, show=False):
	'''
	Plots a contour plot with given parameters. Note that this is just some
	more or less easy way to quickly plot TruSD results. For more sophisticated
	plotting parameters, you might want to copy the function to some local
	script and modify it.

	@param input_file: The file name of the TruSD output to plot
	@param num_trajectories: The number of trajectories. This is only information
		for the title of the plot
	@param s_list: list of selection coefficients
	@param p_list: list of proportions
	@param s_value: selection coefficient to mark on the plot
	@param p_value: proportion to mark on the plot
	@param contour_line_subtract: difference to subtract to draw the contour line.
		Experiement with different values. Set to 0 to remove the contour.
	@param delimiter: Column delimiter of the input file
	@param save: if trueish, save the plot to disk. If this is a string, save to
		that filename. Otherwise, save to `input_file` with pdf as extension.
	@param show: if trueish, show interactive plot
	'''

	values = np.loadtxt(input_file, delimiter=delimiter, unpack=True)

	xlist = s_list #np.arange(-0.08, 0.082, 0.002)
	ylist = p_list #np.arange(0, 1.005, 0.005)

	xmesh, ymesh = np.meshgrid(xlist, ylist)

	max_values = np.max(values)
	min_values = np.min(values)


	levels = np.array([0.5, 0.7, 0.9, 0.95, 0.99, 0.999, 0.9999, 1.0])
	levels = levels * (max_values - min_values) + min_values

	fig, ax = plt.subplots(1, 1, figsize=(15, 15))
	cplot = ax.contourf(xmesh, ymesh, values, levels, colors=[
		'#5affff', '#aaffff', '#d4ffff', '#ffffff', '#ffd5ff', '#ffaaff', '#ff80ff'
	])

	fig.colorbar(cplot, spacing='proportional')

	if contour_line_subtract:
		contour_line = ax.contour(
			xmesh, ymesh, values, [max_values - contour_line_subtract],
			colors=['#000000'], linestyles=['solid']
		)
		ax.clabel(contour_line, inline=1, fontsize=10)

	ax.plot(s_value, p_value, color='#ff0000', marker='o')  # markersize=

	ax.set_title('# Trajectories = {}, s = {}, p = {}'.format(
		num_trajectories, s_value, p_value
	))
	ax.set_xlabel('Selection coefficient, s')
	ax.set_ylabel('Proportion of selected sites, p')

	if save:
		try:
			fig.savefig(save)
		except (AttributeError, IOError):
			outfile = '{}.pdf'.format(input_file.rsplit('.', maxsplit=1)[0])
			print('Python could not save to "{}". Saving to "{}".'.format(save, outfile),
				file=sys.stderr)
			fig.savefig(outfile)

	if show:
		if DISPLAY_PRESENT:
			plt.show()
		else:
			print('Python could not find a DISPLAY. Showing the plot is not supported.',
				file=sys.stderr)
			if not save:
				print('Try to save the plot instead.', file=sys.stderr)


if __name__ == '__main__':
	contour_plot(
		input_file = 'adxwdsdh.csv',
		num_trajectories = 500,
		s_list = np.arange(-0.08, 0.082, 0.002),
		p_list = np.arange(0, 1.005, 0.005),
		s_value = 0.05,
		p_value = 0.1,
		contour_line_subtract = 1.92,
		delimiter = ',',
		save = True,
		show = True
	)
