#!/usr/bin/env python3

import numpy as np
import trusd


filename = 'traj_example.txt'
delimiter = ','  # Delimiter of the fields in the trajectories file
colskip = 2  # Numbers of columns to skip from left in the trajectories file.
             # Skip all columns that are not part of the actual trajectories.
             # With your usual files, colskip should be 2.
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
results = trusd.likelihood_grid(trajectories,
                                genepop=genepop,
                                proportions=properties,
                                selections=sel_coeffs,
                                time_points=time_steps)

# Save results to "outfile"
np.savetxt(outfile, results, delimiter=delimiter)
