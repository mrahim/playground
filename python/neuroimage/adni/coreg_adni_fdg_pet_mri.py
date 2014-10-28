"""
A script that coregisters fdg PET (uniform) to anatomical MRI
"""

import os, glob
import pandas as pd

BASE_DIR = '/disk4t/mehdi/data/pet_fdg_baseline_processed_ADNI'

data = pd.read_csv(os.path.join(BASE_DIR, 'description_file.csv'))

for idx, row in data.iterrows():
    mri_id = ''.join(['I', str(row['Image_ID_x'])])
    pet_id = ''.join(['I', str(row['Image_ID_y'])])
    mri = glob.glob(os.path.join(BASE_DIR, mri_id, '*.nii'))[0]
    pet = glob.glob(os.path.join(BASE_DIR, pet_id, '*.nii'))[0]
    output = os.path.join(BASE_DIR, pet_id, ''.join([pet_id, '_coreg','.nii']))
    cmd = ' '.join(['fsl5.0-flirt',
                    '-searchrx', '-180', '180',
                    '-searchry', '-180', '180',
                    '-searchrz', '-180', '180',
                    '-forcescaling',
                    '-in', pet,
                    '-ref', mri,
                    '-out', output])
    print idx, mri_id, pet_id
    os.system(cmd)