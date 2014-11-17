"""
Some vizualiations of adni pet images
"""
import os, glob
import numpy as np
import pandas as pd
import nibabel as nib
from nilearn.plotting import plot_epi, plot_anat, plot_img, plot_stat_map
from nilearn import image
BASE_DIR = '/disk4t/mehdi/data/pet_fdg_baseline_processed_ADNI'
data = pd.read_csv(os.path.join(BASE_DIR, 'description_file.csv'))

X = np.load('features_regions.npy')

for idx, row in data.iterrows():
    print idx
    pet_id = ''.join(['I', str(row['Image_ID_y'])])
    pet = glob.glob(os.path.join(BASE_DIR, pet_id, 'I*.nii'))[0]
    pet_img = image.reorder_img(pet, resample='nearest')
    
    seg_id = ''.join(['I', str(row['Image_ID_x'])])
    seg = glob.glob(os.path.join(BASE_DIR, seg_id, '*.nii'))[0]
    seg_img = image.reorder_img(seg, resample='nearest')
    
    seg_data = seg_img.get_data()[:, :, :, 0]
    seg_mean = np.zeros(seg_data.shape)
    for val in np.unique(seg_data):
        if val > 0:
            ind = (seg_data == val)
            seg_mean[ind] = X[idx,(val/256)-1]
    
    seg_img = nib.Nifti1Image(seg_mean, seg_img.get_affine())
    plot_stat_map(seg_img, seg_img, colorbar=True,
                  title='-'.join([pet_id, row.DX_Group]),
                  output_file=os.path.join('figures', 'visualization', 'mS'+pet_id))
    """
    plot_img(seg_img, title='-'.join([pet_id, row.DX_Group]),
             output_file=os.path.join('figures', 'visualization', 'S'+pet_id))

    plot_stat_map(pet_img, pet_img, colorbar=True,
                  title='-'.join([pet_id, row.DX_Group]),
                  output_file=os.path.join('figures', 'visualization', pet_id))
                  
    """