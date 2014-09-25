# -*- coding: utf-8 -*-
"""
Auditory fMRI analysis with nipy 
"""

import numpy as np
from nipy.modalities.fmri.glm import GeneralLinearModel
from nipy.modalities.fmri import design_matrix
from nipy.modalities.fmri.experimental_paradigm import BlockParadigm
from scipy import io
import nibabel as nib
import matplotlib.pylab as pl




# input files
BASE_DIR_PREFIX = '/volatile/accounts/mehdi/data/MoAEpilot/fM00223/f'
img = np.zeros((64,64,64,84))
for i in np.arange(16,99):
    img[...,i-16] = nib.load(BASE_DIR_PREFIX+'M00223_0'+str(i)+'.hdr').get_data()[...,0]


# design matrix
conditions = ['rest', 'listen'] * 7
duration = 6*ones(14)
onset = np.arange(0,84,6)

paradigm = BlockParadigm(con_id=conditions, onset=onset, duration=duration)

M = np.zeros(84)
for i in np.arange(6,83,12):
    M[i:i+7]=1

DM = design_matrix.make_dmtx(M,paradigm,hrf_model='Canonical')

"""
M = np.zeros(84)
for i in np.arange(6,83,12):
    M[i:i+7]=1


DM = design_matrix.make_dmtx(M,hrf_model='canonical',add_regs=np.ones(84))
"""

print DM.matrix

pl.close('all')
pl.imshow(DM.matrix)
pl.colorbar()