# -*- coding: utf-8 -*-
"""
T-test on the voxels of two DX groups.
Plot t-maps and p-maps on the voxels.
@author: Mehdi
"""

# 1- Masking data
# 2- T-Testing

import os, glob
import numpy as np
import pandas as pd
import nibabel as nib
from nilearn.input_data import NiftiMasker
from nilearn.plotting import plot_roi, plot_stat_map
from nilearn.mass_univariate import permuted_ols
from scipy import stats


def plot_mask(pet_files, pet_imgs):
    for pi, pf in zip(pet_imgs, pet_files):
        mask_path = os.path.join('figures', 'mask',
                                 pf.split('/')[-1].split('.')[0]) 
        plot_roi(masker.mask_img_, pi, output_file=mask_path,
                 title=pf.split('/')[-1].split('.')[0])



BASE_DIR = '/disk4t/mehdi/data/pet_fdg_baseline_processed_ADNI'
data = pd.read_csv(os.path.join(BASE_DIR, 'description_file.csv'))

pet_files = []
pet_img = []
for idx, row in data.iterrows():
    pet_file = glob.glob(os.path.join(BASE_DIR,
                                      'I' + str(row.Image_ID_y), '*.nii'))
    if len(pet_file)>0:
        pet_files.append(pet_file[0])
        img = nib.load(pet_file[0])
        pet_img.append(img)

masker = NiftiMasker(mask_strategy='epi',
                     mask_args=dict(opening=8))
masker.fit(pet_files)
pet_masked = masker.transform_niimgs(pet_files, n_jobs=4)
pet_masked = np.vstack(pet_masked)
nb_vox = pet_masked.shape[1]

groups = [['AD', 'Normal'], ['AD', 'MCI'], ['MCI', 'LMCI'], ['MCI', 'Normal']]

for gr in groups:
    gr1_idx = data[data.DX_Group == gr[0]].index.values
    gr2_idx = data[data.DX_Group == gr[1]].index.values
    
    gr1_f = pet_masked[gr1_idx, :]
    gr2_f = pet_masked[gr2_idx, :]
    
    t_masked, p_masked = stats.ttest_ind(gr1_f, gr2_f)
    p_masked = - np.log10(p_masked)


    #TODO permuted_ols(gr1_f, gr2_f)
        
    tmap = masker.inverse_transform(t_masked)
    pmap = masker.inverse_transform(p_masked)

    t_path = os.path.join('figures',
                          'tmap_voxel_'+gr[0]+'_'+gr[1]+'_baseline_adni')
    p_path = os.path.join('figures',
                          'pmap_voxel_'+gr[0]+'_'+gr[1]+'_baseline_adni')
    
    plot_stat_map(tmap, tmap, output_file=t_path, black_bg=True)
    plot_stat_map(pmap, pmap, output_file=p_path, black_bg=True)
