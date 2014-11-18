# -*- coding: utf-8 -*-
"""
T-test at cluster level of pairwise DX Groups.
K-means clustering of pet data.
Plot t-maps and p-maps on the voxels.
@author: Mehdi
"""

import os, glob
import numpy as np
import pandas as pd
import nibabel as nib
from nilearn.input_data import NiftiMasker, NiftiLabelsMasker
from nilearn.plotting import plot_img, plot_stat_map
from nilearn.mass_univariate import permuted_ols
from sklearn.cluster import MiniBatchKMeans
from scipy import stats


# 1- mini batch kmeans (define nb_clusters)
# 2- mean intesnity cluster for each subject
# 3- t-test on clusters

###############################################################################

N_CLUSTERS = 1000

BASE_DIR = '/disk4t/mehdi/data/pet_fdg_baseline_processed_ADNI'
MASK_FILE = '/disk4t/mehdi/data/mask/MNI152_T1_2mm_brain_mask_dil.nii.gz'

data = pd.read_csv(os.path.join(BASE_DIR, 'description_file.csv'))

pet_files = []
pet_img = []
for idx, row in data.iterrows():
    pet_file = glob.glob(os.path.join(BASE_DIR,
                                      'I' + str(row.Image_ID_y), 'wI*.nii'))
    if len(pet_file)>0:
        pet_files.append(pet_file[0])
        img = nib.load(pet_file[0])
        pet_img.append(img)

masker = NiftiMasker(mask_strategy='epi',
                     mask_args=dict(opening=1))
masker.fit(pet_files)

pet_data_masked = masker.transform_niimgs(pet_files, n_jobs=1)
pet_data_masked = np.vstack(pet_data_masked)

##############################################################################
# MiniBatch Kmeans
##############################################################################

mbk = MiniBatchKMeans(init='k-means++', n_clusters=N_CLUSTERS,
                      n_init=10, max_no_improvement=10, verbose=0)
mbk.fit(pet_data_masked.T)
mbk_means_labels = mbk.labels_
mbk_means_cluster_centers = mbk.cluster_centers_
mbk_means_labels_unique = np.unique(mbk_means_labels)

mbk_data = masker.inverse_transform(mbk_means_labels)

plot_img(mbk_data)


##############################################################################
# Generate cluster matrix
##############################################################################

x = np.zeros((len(data), N_CLUSTERS))
for idx in np.arange(len(data)):
    for val in mbk_means_labels_unique:
        ind = (mbk_means_labels == val)
        x[idx, val] = np.mean(pet_data_masked[idx, ind])

##############################################################################
# Inference
##############################################################################
groups = [['AD', 'Normal'], ['AD', 'MCI'], ['MCI', 'LMCI'], ['MCI', 'Normal']]

for gr in groups:
    gr1_idx = data[data.DX_Group == gr[0]].index.values
    gr2_idx = data[data.DX_Group == gr[1]].index.values

    """    
    gr1_f = x[gr1_idx, :]
    gr2_f = x[gr2_idx, :]
    t_clustered, p_clustered = stats.ttest_ind(gr1_f, gr2_f)
    p_clustered = - np.log10(p_clustered)
    """

    gr_idx = np.hstack([gr1_idx, gr2_idx])        
    gr_f = x[gr_idx, :]
    gr_labels = np.vstack([np.hstack([[1]*len(gr1_idx), [0]*len(gr2_idx)]),
                           np.hstack([[0]*len(gr1_idx), [1]*len(gr2_idx)])]).T

    
    p_clustered, t_clustered, _ = permuted_ols(gr_labels, gr_f,
                                              n_perm=1000, n_jobs=4,
                                              model_intercept=True)


    t_masked = np.zeros(pet_data_masked.shape[1])
    p_masked = np.zeros(pet_data_masked.shape[1])
    for val in mbk_means_labels_unique:
        t_masked[(mbk_means_labels == val)] = t_clustered[0, val]
        p_masked[(mbk_means_labels == val)] = p_clustered[0, val]
            
    tmap = masker.inverse_transform(t_masked)
    pmap = masker.inverse_transform(p_masked)
    
    
    plot_stat_map(tmap, tmap,
                  black_bg=True, title='/'.join(gr), cut_coords=(1,-21,11))
    plot_stat_map(pmap, pmap,
                  black_bg=True, title='/'.join(gr), cut_coords=(1,-21,11))
    tmap.to_filename('tmap_kmeans.nii')
    pmap.to_filename('pmap_kmeans.nii')
    
    break
    """
    gr_idx = np.hstack([gr1_idx, gr2_idx])        
    gr_f = x[gr_idx, :]
    gr_labels = np.vstack([np.hstack([[1]*len(gr1_idx), [0]*len(gr2_idx)]),
                           np.hstack([[0]*len(gr1_idx), [1]*len(gr2_idx)])]).T
    
    neg_log_pvals, t_scores, _ = permuted_ols(gr_labels, gr_f,
                                              n_perm=1000, n_jobs=4,
                                              model_intercept=True)
    """                                              

    