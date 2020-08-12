#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt


filename = 'adxwdsdh.csv'
num_trajectories = 500  # The number of trajectories
s_value = 0.05          # Proportion of selected sites
p_value = 0.1           # Selection coefficient

contour_line_subtract = 1.92  # Somewhat strange value to subtract from maximum to draw coutour line
                              # Set to 0 to hide contour line


def contour_plot(filename, num_trajectories, s_value, p_value, contour_line_subtract, save=True, show=False):

	values = np.loadtxt(filename, delimiter=',', unpack=True)

	xlist = np.arange(-0.08, 0.082, 0.002)
	ylist = np.arange(0, 1.005, 0.005)

	X, Y = np.meshgrid(xlist, ylist)

	max_values = np.max(values)
	min_values = np.min(values)


	levels = np.array([0.5, 0.7, 0.9, 0.95, 0.99, 0.999, 0.9999, 1.0])
	levels = levels * (max_values - min_values) + min_values

	fig, ax = plt.subplots(1, 1, figsize=(15, 15))
	contour_plot = ax.contourf(X, Y, values, levels, colors=['#5affff', '#aaffff', '#d4ffff', '#ffffff', '#ffd5ff', '#ffaaff', '#ff80ff'])

	fig.colorbar(contour_plot)

	if contour_line_subtract:
		contour_line = ax.contour(X, Y, values, [max_values - contour_line_subtract], colors=['#000000'], linestyles=['solid'])
		ax.clabel(contour_line, inline=1, fontsize=10)

	single_point = ax.plot(s_value, p_value, color='#ff0000', marker='o')  # markersize=

	ax.set_title('# Trajectories = {}, s = {}, p = {}'.format(num_trajectories, s_value, p_value))
	ax.set_xlabel('Selection coefficient, s')
	ax.set_ylabel('Proportion of selected sites, p')

	if save:
		fig.savefig('{}.pdf'.format(filename.rsplit('.', maxsplit=1)[0]))

	if show:
		plt.show()


if __name__ == '__main__':
	contour_plot(filename, num_trajectories, s_value, p_value, contour_line_subtract)
