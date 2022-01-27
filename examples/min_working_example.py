#!/usr/bin/env python3

import numpy as np
import trusd


filename = 'traj_example.txt'
delimiter = ','  # Delimiter of the fields in the trajectories file
colskip = 2  # Numbers of columns to skip from left in the trajectories file.
             # Skip all columns that are not part of the actual trajectories.
             # For the example file, colskip should be 2.

genepop = 200  # NE

# Properties (from 0 to 1 with 0.005 steps)
properties = np.arange(0, 1.001, 0.005)

# Selection coefficients (from -0.08 to 0.08 with 0.002 steps)
sel_coeffs = np.arange(-0.08, 0.081, 0.002)

time_steps = [0, 25, 50]  # Time steps
outfile = 'outfile.txt'  # Output file name


# Read trajectory file as numpy array
trajectories = trusd.read_trajectory_file(filename,
                                          delimiter=delimiter,
                                          skip_columns=colskip)

# Calculate results (this step will take a lot of time!)
best_s, best_p, best_l = trusd.run_analysis(trajectories,
                                            genepop=genepop,
                                            proportions=properties,
                                            selections=sel_coeffs,
                                            time_points=time_steps,
                                            save_output=outfile)

print(f'Best (s, p) is ({best_s:.5f}, {best_p:.5f}) with likelihood {best_l}')

# Save metadata to "outfile".json
metadata_file = trusd.write_info_file(filename, outfile, __file__,
                                      genepop, len(trajectories), time_steps,
                                      properties, sel_coeffs,
                                      {'s': best_s, 'p': best_p, 'likelihood': best_l},
                                      delimiter)

plot_file = '{}.pdf'.format(outfile.rsplit('.', maxsplit=1)[0])

# Plot the results
trusd.plot_from_metadata(metadata_file=metadata_file,
                         contour_line_subtract=1.92, save=plot_file)
