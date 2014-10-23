# -*- coding: utf-8 -*-
"""
A script that uses nilearn to resample a segmentation image
"""

import os, glob, time
import nibabel as nib
from nilearn import plotting, image



input_filename = ''.join(['/disk4t/mehdi/data/pet_fdg_baseline_processed_ADNI/',
                          'I218153/ADNI_011_S_0183_MR_MAPER_segmentation',
                          ',_masked_Br_20110218145719200_S12000_I218153.nii'])
                 

original_img = nib.load(input_filename)
ord_img = image.reorder_img(original_img, resample=True)

close('all')
plotting.plot_img(ord_img)