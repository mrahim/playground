# -*- coding: utf-8 -*-
"""
Canonical ICA on ADNI groups (AD, LMCI, MCI, Normal)
@author: Mehdi
"""

import os, glob
import numpy as np
import pandas as pd
import nibabel as nib
from nilearn.plotting import plot_stat_map
from nilearn.decomposition.canica import CanICA

BASE_DIR = '/disk4t/mehdi/data/pet_fdg_baseline_processed_ADNI'

data = pd.read_csv(os.path.join(BASE_DIR, 'description_file.csv'))

pet_files = []
pet_img = []

for idx, row in data.iterrows():
    pet_file = glob.glob(os.path.join(BASE_DIR,
                                      'I' + str(row.Image_ID_y), 'wI*.nii'))
    if len(pet_file)>0:
        pet_files.append(pet_file[0])
        img = nib.load(pet_file[0])
        if idx == 0:
            data4d = np.expand_dims(img.get_data(), axis=3)
        else:
            data4d = np.concatenate((data4d,
                                     np.expand_dims(img.get_data(), axis=3)),
                                    axis=3)

pet_files = np.array(pet_files)
img4d = nib.Nifti1Image(data4d, img.get_affine())

groups = ['AD', 'LMCI', 'MCI', 'Normal']
    
n_components = 20
canica = CanICA(n_components=n_components,
                memory="nilearn_cache", memory_level=5,
                threshold='auto', verbose=10, random_state=0)
canica.fit(img4d)

print 'inverse'

components_img = canica.masker_.inverse_transform(canica.components_)
components_img.to_filename('figures/canica_'+str(n_components)+'.nii.gz')

for i in range(n_components):
    plot_stat_map(nib.Nifti1Image(components_img.get_data()[..., i],
                                      components_img.get_affine()),
                  display_mode="z", title="IC %d"%i, cut_coords=1,
                  colorbar=False)
