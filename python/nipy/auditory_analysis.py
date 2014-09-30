# -*- coding: utf-8 -*-
"""
Auditory fMRI analysis with nipy
"""

import os

import numpy as np

import nibabel as nib

from nipy.modalities.fmri.glm import FMRILinearModel
from nipy.modalities.fmri import design_matrix
from nipy.modalities.fmri.experimental_paradigm import BlockParadigm

from pypreprocess.reporting import glm_reporter


# input image
BASE_DIR = '/volatile/accounts/mehdi/data/examples/MoAEpilot/'
input_image = nib.load(BASE_DIR + 'fM00223/4D-preproc.nii')

# design matrix
TR = 7
N_SCANS = 84

conditions = ['listen'] * 7
duration = TR * 6 * np.ones(7)

onset = np.arange(6, N_SCANS, 12) * TR
paradigm = BlockParadigm(con_id=conditions,
                         onset=onset,
                         duration=duration)
frametimes = np.linspace(0, (N_SCANS - 1) * TR, N_SCANS)

design_mat = design_matrix.make_dmtx(frametimes, paradigm,
                                     hrf_model='Canonical',
                                     drift_model='Cosine',
                                     hfcut=168)
design_mat.show()


# general linear model
glm = FMRILinearModel(input_image, design_mat.matrix, mask='compute')
glm.fit()



# contrasts
c = np.hstack([1, np.zeros(len(design_mat.names)-1)])

z_map, t_map, eff_map, var_map = glm.contrast(c,
                                              contrast_type='t',
                                              output_z=True,
                                              output_stat=True,
                                              output_effects=True,
                                              output_variance=True)

# save maps
for result, filename in zip([z_map, t_map, eff_map, var_map],
                            ['z_map', 't_map', 'eff_map', 'var_map']):
    nib.save(result, os.path.join(BASE_DIR, 'results', 'maps', filename))

# glm reporting
contrasts = {'Listen': 1}
zmaps = {'Listen': os.path.join(BASE_DIR, 'results', 'maps', 'z_map.nii')}

glm_reporter.generate_subject_stats_report(
    os.path.join(BASE_DIR, 'results', 'reports', 'report.html'),
    contrasts,
    zmaps,
    glm.mask)