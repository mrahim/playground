# -*- coding: utf-8 -*-
"""
Auditory fMRI analysis with nipy 
"""

import os
import numpy as np
from nipy.modalities.fmri.glm import GeneralLinearModel
from nipy.modalities.fmri import design_matrix
from nipy.modalities.fmri.experimental_paradigm import BlockParadigm
from nipy.modalities.fmri.glm import FMRILinearModel
from scipy import io
import nibabel as nib
import matplotlib.pylab as pl
from nipy.labs.viz import plot_map, mni_sform, coord_transform

# input image
BASE_DIR_PREFIX = '/volatile/accounts/mehdi/data/MoAEpilot/'
image = nib.load(BASE_DIR_PREFIX+'fM00223/4D-smoothed.nii')

# design matrix
conditions = ['listen'] * 7
duration = 6*np.ones(7)
onset = np.arange(6,84,12)
paradigm = BlockParadigm(con_id=conditions, onset=onset, duration=duration)
frametimes = np.arange(6,90)

DM = design_matrix.make_dmtx(frametimes,paradigm,hrf_model='Canonical',
                             drift_model='blank')


# GLM

GLM = FMRILinearModel(image,DM.matrix)
GLM.fit()


# Contrast
c = np.array([1,0])

z_map, t_map, eff_map, var_map  = GLM.contrast(c,
                 contrast_type='t',
                 output_z=True,
                 output_stat=True,
                 output_effects=True,
                 output_variance=True
                 )

for result,filename in zip([z_map, t_map, eff_map, var_map],
                  ['z_map', 't_map', 'eff_map', 'var_map']):
    nib.save(result,os.path.join(BASE_DIR_PREFIX,'results',filename)) 