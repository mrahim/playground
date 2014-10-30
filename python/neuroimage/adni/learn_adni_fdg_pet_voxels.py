"""
A script that :
- extracts voxels from FDG PET (baseline, uniform)
- reduces dimension and learn
"""

import os, glob
import numpy as np
import pandas as pd
import nibabel as nib

BASE_DIR = '/disk4t/mehdi/data/pet_fdg_baseline_processed_ADNI'

data = pd.read_csv(os.path.join(BASE_DIR, 'description_file.csv'))
S = np.zeros((len(data), 83))
for idx, row in data.iterrows():
    pet_id = ''.join(['I', str(row['Image_ID_y'])])
    pet = glob.glob(os.path.join(BASE_DIR, pet_id, '*.nii.gz'))[0]
    
    seg_id = ''.join(['I', str(row['Image_ID_x'])])
    seg = glob.glob(os.path.join(BASE_DIR, seg_id, '*.nii'))[0]
    
    pet_img = nib.load(pet)
    seg_img = nib.load(seg)

    pet_data = pet_img.get_data()
    seg_data = seg_img.get_data()[:, :, :, 0]    
    
    for val in np.unique(seg_data):
        if val > 0:
            ind = (seg_data == val)
            S[idx,(val/256)-1] = np.mean(pet_data[ind])
            break
    break