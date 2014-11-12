"""
    Plotting PSYDAT alignment results
"""

import os, glob
from pypreprocess.reporting.check_preprocessing import plot_spm_motion_parameters

BASE_DIR = os.path.join('/', 'shfj', 'Ppsypim', 'PSYDAT', 'Subjects')
FIG_BASE_DIR = os.path.join('figures')

subject_path_list = glob.glob(os.path.join(BASE_DIR, 'S*'))

for sp in subject_path_list:
    root, subject_id = os.path.split(sp)

    mid_dir = os.path.join(sp, 'MRI', 'MID')
    if os.path.isdir(mid_dir):
        # Plot Realign
        mvt = glob.glob(os.path.join(mid_dir, '*.txt'))
        if len(mvt)>0:
            realign_fig = os.path.join(FIG_BASE_DIR, 'realign', subject_id)
            plot_spm_motion_parameters(mvt[0],
                                       title=subject_id,
                                       output_filename=realign_fig)
