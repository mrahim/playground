"""
Plotting T1MRI
"""
import os, glob
from nilearn import plotting, image

BASE_DIR = os.path.join('/', 'shfj', 'Ppsypim', 'PSYDAT', 'Subjects')
OUPUT_DIR = os.path.join('figures')

subject_list = os.listdir(BASE_DIR)

for subject_id in subject_list:
    print subject_id
    # fMRI
    """
    fmri_path = os.path.join(BASE_DIR, subject_id, 'MRI', 'MID')
    fmri_list = glob.glob(os.path.join(fmri_path, '[E-S]*.nii'))
    """

    # MRI        
    anat_path = os.path.join(BASE_DIR, subject_id, 'MRI', 'T1MRI')
    anat_list = glob.glob(os.path.join(anat_path, '*.hdr'))
    
    if len(anat_list)>0:      
        anat_name = '_'.join([subject_id, 'anat'])
        r_img_anat = image.reorder_img(anat_list[0], resample='continuous')
        
        plotting.plot_anat(r_img_anat,
                          output_file=os.path.join(OUPUT_DIR, 't1mri', anat_name),
                          title=anat_name,
                          black_bg=True)