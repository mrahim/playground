"""
WARD clustering of ADNI Baseline FDG-PET
"""

import os, glob
import numpy as np
import pandas as pd
import nibabel as nib
from nilearn.input_data import NiftiMasker
from nilearn.plotting import plot_stat_map, plot_roi
from sklearn.feature_extraction import image
from sklearn.cluster import WardAgglomeration
import time

BASE_DIR = '/disk4t/mehdi/data/pet_fdg_baseline_processed_ADNI'

data = pd.read_csv(os.path.join(BASE_DIR, 'description_file.csv'))

pet_files = []
pet_img = []
for idx, row in data.iterrows():
    pet_file = glob.glob(os.path.join(BASE_DIR,
                                      'I' + str(row.Image_ID_y), 'I*.nii'))
    if len(pet_file)>0:
        pet_files.append(pet_file[0])
        img = nib.load(pet_file[0])
        pet_img.append(img)

masker = NiftiMasker(mask_strategy='epi',
                     mask_args=dict(opening=8))
masker.fit(pet_files)

pet_masked = masker.transform_niimgs(pet_files, n_jobs=2)
#pet_masked = np.vstack(pet_masked)


mask = masker.mask_img_.get_data().astype(np.bool)
shape = mask.shape
connectivity = image.grid_to_graph(n_x=shape[0], n_y=shape[1],
                                   n_z=shape[2], mask=mask)

# Computing the ward for the first time, this is long...
start = time.time()
ward = WardAgglomeration(n_clusters=1000, connectivity=connectivity,
                         memory='nilearn_cache')
ward.fit(pet_masked[0])
print "Ward agglomeration 1000 clusters: %.2fs" % (time.time() - start)


labels = ward.labels_ + 1
labels_img = masker.inverse_transform(labels)
first_plot = plot_roi(labels_img, pet_img[0], title="Ward parcellation",
                      display_mode='xz')
# labels_img is a Nifti1Image object, it can be saved to file with the
# following code:
labels_img.to_filename('parcellation.nii')


"""
##################################################################
# Compute the ward with more clusters, should be faster as we are using
# the caching mechanism
start = time.time()
ward = WardAgglomeration(n_clusters=2000, connectivity=connectivity,
                         memory='nilearn_cache')
ward.fit(fmri_masked)
print "Ward agglomeration 2000 clusters: %.2fs" % (time.time() - start)
"""