"""
    Plotting PSYDAT coregirstration results
"""

import os, glob
from pypreprocess.reporting.check_preprocessing import plot_registration
from pypreprocess import coreg

BASE_DIR = os.path.join('/', 'shfj', 'Ppsypim', 'PSYDAT', 'Subjects')
FIG_BASE_DIR = os.path.join('figures')

subject_path_list = glob.glob(os.path.join(BASE_DIR, 'S*'))

for sp in subject_path_list:
    root, subject_id = os.path.split(sp)

    # Plot Coreg
    mid_dir = os.path.join(sp, 'MRI', 'MID')
    fmri = glob.glob(os.path.join(mid_dir, '[se]*.nii'))
    
    t1_dir = os.path.join(sp, 'MRI', 'T1MRI')
    t1mri = glob.glob(os.path.join(t1_dir, '*.hdr'))


    coreg_fig = os.path.join(FIG_BASE_DIR, 'coregister', subject_id)
    if len(fmri)>0 and len(t1mri)>0:
        c = coreg.Coregister()
        c.fit(fmri[0], t1mri[0])
        transf = c.transform(t1mri[0])
        plot_registration(transf, fmri[0], 
                          title=subject_id,
                          output_filename=coreg_fig)
                          
                          
                          
                          
