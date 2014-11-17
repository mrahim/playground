# -*- coding: utf-8 -*-
"""
A script that checks nii images by:
    - Fetching image size and resolution
    - Computing histogram
"""
import os, glob
import nibabel as nib
import matplotlib.pyplot as plt
from nilearn import plotting, image

BASE_DIR = '/disk4t/mehdi/data/pet_fdg_baseline_processed_ADNI'
plt.close('all')

counter = 0
error_counter = 0
for root, dirs, files in os.walk(BASE_DIR):    
    for d in dirs:
        current_folder = os.path.join(root, d)
        # Load nii image
        filename = glob.glob(os.path.join(current_folder, '*.nii'))
        img = nib.load(filename[0])
        # prepare output image name
        output_fig_name = d
        counter += 1
        plt.clf
        print output_fig_name
        try:
            image.reorder_img(img)
            '''
            plotting.plot_img(img,
                  output_file=os.path.join('figs', output_fig_name),
                  title=str(img.shape),
                  black_bg=True)            
            '''
        except ValueError as exc:
                        
            ord_img = image.reorder_img(img, resample='nearest')
            resampled_image = image.resample_img(ord_img)
            affine = np.eye(4)
            plotting.plot_img(nib.Nifti1Image(img.get_data(), affine),
                  output_file=os.path.join('figures/visualization', output_fig_name+'x'),
                  title=str(img.shape),
                  black_bg=True)
            plotting.plot_img(ord_img,
                  output_file=os.path.join('figures/visualization', output_fig_name),
                  title=str(img.shape),
                  black_bg=True)
            ord_img.to_filename(os.path.join('figures/visualization', output_fig_name+'.nii'))
            error_counter += 1
            print str(filename[0])
            

print '{}/{} errors'.format(error_counter, counter) 


'''

# Compute histogram
img_data = img.get_data().ravel()
n, bins, patches = pl.hist(img_data, bins=100,
                           range=(0.02, img_data.max()),
                           normed=1, histtype='bar', rwidth=0.8)
pl.savefig(os.path.join('figs', output_fig_name + '_hist'))
pl.close('all')
'''