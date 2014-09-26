# -*- coding: utf-8 -*-
"""
Auditory fMRI analysis with nipy 
"""

import os

import numpy as np
from scipy import io
import matplotlib.pylab as pl

import nibabel as nib

from nipy.labs.viz import plot_map, mni_sform, coord_transform
from nipy.modalities.fmri.glm import GeneralLinearModel, FMRILinearModel
from nipy.modalities.fmri import design_matrix
from nipy.modalities.fmri.experimental_paradigm import BlockParadigm

from pypreprocess.reporting import glm_reporter


# input image
BASE_DIR_PREFIX = '/volatile/accounts/mehdi/data/MoAEpilot/'
input_image = nib.load(BASE_DIR_PREFIX + 'fM00223/4D-smoothed.nii')

# design matrix
TR = 7
n_scans = 84
epoch_duration = 6

conditions = ['listen'] * 7
duration = TR * 6 * np.ones(7)
onset = np.arange(6, n_scans, 12) * TR
paradigm = BlockParadigm(con_id=conditions, onset=onset, duration=duration)
frametimes = np.linspace(0, (n_scans - 1) * TR, n_scans)

designmatrix = design_matrix.make_dmtx(frametimes, paradigm, 
                                       hrf_model='Canonical',
                                       drift_model='Cosine', 
                                       hfcut=128)
designmatrix.show()

# GLM
glm = FMRILinearModel(input_image, designmatrix.matrix, mask='compute')
glm.fit()

# Contrast
c = np.hstack([1, np.zeros(7)])

z_map, t_map, eff_map, var_map  = GLM.contrast(
                 c,
                 contrast_type='t',
                 output_z=True,
                 output_stat=True,
                 output_effects=True,
                 output_variance=True
                 )

# Save maps
for result,filename in zip([z_map, t_map, eff_map, var_map],
                  ['z_map', 't_map', 'eff_map', 'var_map']):
    nib.save(result,os.path.join(BASE_DIR_PREFIX,'results','maps',filename)) 
    
# GLM Reporting
contrasts = {'Listen':1}
zmaps = {'Listen':os.path.join(BASE_DIR_PREFIX,'results','maps','z_map.nii')}

glm_reporter.generate_subject_stats_report(
                os.path.join(BASE_DIR_PREFIX,'results','reports','report.html'),
                contrasts,
                zmaps,
                glm.mask)