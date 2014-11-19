# -*- coding: utf-8 -*-
"""
T-test at cluster level of pairwise DX Groups.
K-means clustering of pet data.
Plot t-maps and p-maps on the voxels.
@author: Mehdi
"""

import os, glob
import matplotlib.cm as cm
import numpy as np
import pandas as pd
import nibabel as nib
from nilearn.input_data import NiftiMasker
from nilearn.plotting import plot_img, plot_stat_map
from nilearn.mass_univariate import permuted_ols
from sklearn.cluster import MiniBatchKMeans
from scipy import stats

# 1- mini batch kmeans (define nb_clusters)
# 2- mean intesnity cluster for each subject
# 3- t-test on clusters

###############################################################################


N_CLUSTERS_SET = [500, 1000, 1500, 2000]
SPATIAL_NEIGHBORHOOD_SET = [False]
USE_CENTROIDS_SET = [False]
"""
N_CLUSTERS = 83
SPATIAL_NEIGHBORHOOD = False
USE_CENTROIDS = False
"""
BASE_DIR = '/disk4t/mehdi/data/pet_fdg_baseline_processed_ADNI'
MNI_TEMPLATE = os.path.join(BASE_DIR, 'wMNI152_T1_2mm_brain.nii')

data = pd.read_csv(os.path.join(BASE_DIR, 'description_file.csv'))

pet_files = []
pet_img = []
for idx, row in data.iterrows():
    pet_file = glob.glob(os.path.join(BASE_DIR,
                                      'I' + str(row.Image_ID_y), 'wI*.nii'))
    if len(pet_file) > 0:
        pet_files.append(pet_file[0])
        img = nib.load(pet_file[0])
        pet_img.append(img)

masker = NiftiMasker(mask_strategy='epi',
                     mask_args=dict(opening=1))
masker.fit(pet_files)

pet_data_masked = masker.transform_niimgs(pet_files, n_jobs=4)
pet_data_masked = np.vstack(pet_data_masked)

"""
Test various n_clusters
"""
for USE_CENTROIDS in USE_CENTROIDS_SET:
    for SPATIAL_NEIGHBORHOOD in SPATIAL_NEIGHBORHOOD_SET:
        for N_CLUSTERS in N_CLUSTERS_SET:
            
            if SPATIAL_NEIGHBORHOOD:
                img_shape = masker.mask_img_.shape
                x,y,z = np.meshgrid(np.arange(img_shape[1]),
                                    np.arange(img_shape[0]),
                                    np.arange(img_shape[2]))
                                    
                x_img = nib.Nifti1Image(x, masker.affine_)
                y_img = nib.Nifti1Image(y, masker.affine_)
                z_img = nib.Nifti1Image(z, masker.affine_)
                
                loc = masker.transform([x_img, y_img, z_img])
            else:
                loc = np.zeros((0, pet_data_masked.shape[1]))
            
            
            ##############################################################################
            # MiniBatch Kmeans
            ##############################################################################
            
            mbk = MiniBatchKMeans(init='k-means++', n_clusters=N_CLUSTERS,
                                  n_init=10, max_no_improvement=10, verbose=0)
            
            pet_loc_data = np.concatenate((pet_data_masked.T, loc.T), axis=1)
            
            mbk.fit(pet_loc_data)
            mbk_means_labels = mbk.labels_
            mbk_means_cluster_centers = mbk.cluster_centers_
            mbk_means_labels_unique = np.unique(mbk_means_labels)
            
            mbk_data = masker.inverse_transform(mbk_means_labels)
            
            plot_img(mbk_data)
            
            
            ##############################################################################
            # Generate cluster matrix
            ##############################################################################
            
            if USE_CENTROIDS:
                x = mbk_means_cluster_centers[:, :96].T
            else:
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
            
                gr1_f = x[gr1_idx, :]
                gr2_f = x[gr2_idx, :]
                tval_clustered, pval_clustered = stats.ttest_ind(gr1_f, gr2_f)
                pval_clustered = - np.log10(pval_clustered)
            
                gr_idx = np.hstack([gr1_idx, gr2_idx])
                gr_f = x[gr_idx, :]
                gr_labels = np.vstack([np.hstack([[1]*len(gr1_idx), [0]*len(gr2_idx)]),
                                       np.hstack([[0]*len(gr1_idx), [1]*len(gr2_idx)])]).T
            
                p_clustered, t_clustered, _ = permuted_ols(gr_labels, gr_f,
                                                           n_perm=1000, n_jobs=4,
                                                           model_intercept=True)
            
                t_masked = np.zeros(pet_data_masked.shape[1])
                p_masked = np.zeros(pet_data_masked.shape[1])
                pval_masked = np.zeros(pet_data_masked.shape[1])
                for val in mbk_means_labels_unique:
                    t_masked[(mbk_means_labels == val)] = t_clustered[0, val]
                    p_masked[(mbk_means_labels == val)] = p_clustered[0, val]
                    pval_masked[(mbk_means_labels == val)] = pval_clustered[val]
            
                tmap = masker.inverse_transform(t_masked)
                pmap = masker.inverse_transform(p_masked)
                pvalmap = masker.inverse_transform(pval_masked)
                header = pmap.get_header()
                header['aux_file'] = 'Hot'
                header = pvalmap.get_header()
                header['aux_file'] = 'Hot'
            
                t_nii_filename = '_'.join(['tmap', 'kmeans', str(N_CLUSTERS)])
                t_nii_filename += '_' + '_'.join(gr)    
                p_nii_filename = '_'.join(['pmap', 'kmeans', str(N_CLUSTERS)])
                p_nii_filename += '_' + '_'.join(gr)
                pval_nii_filename = '_'.join(['pvalmap', 'kmeans', str(N_CLUSTERS)])
                pval_nii_filename += '_' + '_'.join(gr)
                
                if SPATIAL_NEIGHBORHOOD:
                    t_nii_filename += '_s'
                    p_nii_filename += '_s'
                    pval_nii_filename += '_s'
                if USE_CENTROIDS:
                    t_nii_filename += '_c'
                    p_nii_filename += '_c'
                    pval_nii_filename += '_c'
                t_fig_filename = t_nii_filename
                p_fig_filename = p_nii_filename
                pval_fig_filename = pval_nii_filename
                t_nii_filename += '.nii'
                p_nii_filename += '.nii'
                pval_nii_filename += '.nii'
            
                tmap.to_filename(os.path.join('figures', 'nii', t_nii_filename))
                pmap.to_filename(os.path.join('figures', 'nii', p_nii_filename))
                pvalmap.to_filename(os.path.join('figures', 'nii', pval_nii_filename))
            
                plot_stat_map(tmap, MNI_TEMPLATE, threshold=None, cmap=cm.bwr,
                              output_file=os.path.join('figures', 'tmap', t_fig_filename),
                              black_bg=True, title='/'.join(gr))
            
                plot_img(pmap, bg_img=MNI_TEMPLATE, threshold=None,
                         colorbar=True, cmap=cm.hot, vmin=0,
                         output_file=os.path.join('figures', 'pmap', p_fig_filename),
                         black_bg=True, title='/'.join(gr))
                         
                plot_img(pvalmap, bg_img=MNI_TEMPLATE, threshold=None,
                         colorbar=True, cmap=cm.hot, vmin=0,
                         output_file=os.path.join('figures', 'pmap', pval_fig_filename),
                         black_bg=True, title='/'.join(gr))
                break
