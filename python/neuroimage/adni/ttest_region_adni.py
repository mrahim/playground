# -*- coding: utf-8 -*-
"""
T-test on (83) regions of two DX groups.
Plot t-maps and p-maps on the (83) regions
@author: Mehdi
"""

import os, glob
import numpy as np
import pandas as pd
from scipy import stats
import nibabel as nib
import matplotlib.cm as cm
from nilearn import plotting, image



BASE_DIR = '/disk4t/mehdi/data/pet_fdg_baseline_processed_ADNI/'

data = pd.read_csv(os.path.join(BASE_DIR, 'description_file.csv'))
x = np.load('features_regions.npy')


groups = [['AD', 'Normal'], ['AD', 'MCI'], ['MCI', 'LMCI'], ['MCI', 'Normal']]

for gr in groups:

    gr1_idx = data[data.DX_Group == gr[0]].index.values
    gr2_idx = data[data.DX_Group == gr[1]].index.values
    
    gr1_f = x[gr1_idx, :]
    gr2_f = x[gr2_idx, :]

    t = [0]*83
    p = [0]*83
    for i in np.arange(83):
        t[i], p[i] = stats.ttest_ind(gr1_f[:, i], gr2_f[:, i])
    
    # plot t-maps on the brain segmentation
    seg_path = glob.glob(os.path.join(BASE_DIR, 'I221122', '*.nii'))
    seg_img = nib.load(seg_path[0])
    seg_img = image.reorder_img(seg_img, resample='nearest')

    if len(seg_img.shape)==4:
        seg_data = seg_img.get_data()[:, :, :, 0]
    else:
        seg_data = seg_img.get_data()
        
    t_data = np.zeros(seg_data.shape)
    p_data = np.zeros(seg_data.shape)
    idx = 0
    for val in np.unique(seg_data):
        if val > 0:
            t_data[(seg_data == val)] = t[idx]
            p_data[(seg_data == val)] = -np.log10(p[idx])
            idx += 1
            
    t_img = nib.Nifti1Image(t_data, seg_img.get_affine())
    p_img = nib.Nifti1Image(p_data, seg_img.get_affine())
    
    print np.max(t_data), np.min(t_data)
    print np.max(p_data), np.min(p_data)
    
    t_path = os.path.join('figures', 'tmap_'+gr[0]+'_'+gr[1]+'_baseline_adni_region')
    p_path = os.path.join('figures', 'pmap_'+gr[0]+'_'+gr[1]+'_baseline_adni_region')
    plotting.plot_img(t_img, black_bg=True, cmap=cm.bwr, title='/'.join(gr),
                      output_file=t_path, cut_coords=[0, 36, 0],
                      colorbar=True, vmin=-6.4, vmax=6.4)
    plotting.plot_stat_map(p_img, p_img, black_bg=True, title='/'.join(gr),
                      output_file=p_path, cut_coords=[0, 36, 0])
