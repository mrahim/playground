"""
    Routines for plotting p-maps and t-maps
    Requires:
    - Pmap or Tmap
    - MNI T-1 template
"""
import os
import numpy as np
import nibabel as nib
from nilearn.plotting import  plot_img, cm
import matplotlib.cm as cmap


def plot_tmaps():
    for gr in groups:
        filename = '_'.join(['tmap', 'voxel',
                             'norm', '_'.join(gr), 'baseline',
                             'adni' ]) + '.nii'
        nii_img = os.path.join( NII_DIR, filename)
        for ext in ['.png', '.pdf', '.svg']:
            try:
                print np.max(nib.load(nii_img).get_data())
                vm = 7
                plot_img(nii_img, bg_img=MNI_TEMPLATE, cmap=cm.cold_hot,
                         black_bg=True, threshold=4,
                         cut_coords=(0, -45, 32),
                         output_file=os.path.join('figures', 'release',
                                                  filename.split('.')[0])+ext,
                         vmin = -vm, vmax=vm,
                         title='/'.join(gr), colorbar=True)
            except ValueError:
                plot_img(nii_img, bg_img=MNI_TEMPLATE, cmap=cm.cold_hot,
                         black_bg=True, threshold='auto',
                         cut_coords=(0, -45, 32),
                         output_file=os.path.join('figures', 'release',
                                                  filename.split('.')[0])+ext,
                         vmin = -vm, vmax=vm,
                         title='/'.join(gr), colorbar=True)



def plot_pmaps():
    for gr in groups:
        filename = '_'.join(['pmap', 'voxel',
                             'norm', '_'.join(gr), 'baseline',
                             'adni' ]) + '.nii'
        nii_img = os.path.join( NII_DIR, filename)
        for ext in ['.png', '.pdf', '.svg']:
            try:
                print np.max(nib.load(nii_img).get_data())
                vm = 8
                plot_img(nii_img, bg_img=MNI_TEMPLATE,
                         colorbar=True, cmap=cmap.hot,
                         cut_coords=(0, -45, 32),
                         output_file=os.path.join('figures', 'release',
                                                  filename.split('.')[0])+ext,
                         black_bg=True, threshold=5, vmin=0, vmax=vm,
                         title='/'.join(gr))
            except ValueError:
                plot_img(nii_img, bg_img=MNI_TEMPLATE,
                         colorbar=True, cmap=cmap.hot,
                         cut_coords=(0, -45, 32),
                         output_file=os.path.join('figures', 'release',
                                                  filename.split('.')[0])+ext,
                         black_bg=True, threshold=2, vmin=0, vmax=vm,
                         title='/'.join(gr))

BASE_DIR = '/disk4t/mehdi/data/pet_fdg_baseline_processed_ADNI'
#BASE_DIR = '/disk4t/mehdi/data/ADNI_baseline_fdg_pet'
NII_DIR = os.path.join('figures', 'nii')

MNI_TEMPLATE = os.path.join(BASE_DIR, 'wMNI152_T1_2mm_brain.nii')

groups = [['AD', 'Normal'], ['AD', 'MCI'], ['MCI', 'LMCI'], ['MCI', 'Normal']]

plot_pmaps()