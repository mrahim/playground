"""
A script that renames MID and T1MRI data :
- S[xxxxx]_s005[000i].nii
- S[xxxxx]_struct.hdr, .img

Added : a plotting of the T1MRI data
"""

import os, glob
import nibabel as nib
from nilearn import image, plotting

BASE_DIR = os.path.join('/', 'home', 'Ppsypim', 'PSYDAT', 'Subjects')

for subject in os.listdir(BASE_DIR):
    mid_path = os.path.join(BASE_DIR, subject, 'MRI', 'MID')
    mid_files = glob.glob(os.path.join(mid_path, '[a-z|A-Z]*.txt'))
    for f in mid_files:
        filedir, filename = os.path.split(f)
        filename = f.split('/')[-1]
        if 'Exam' in filename:
            new_filename = filename.replace('Exam','S')
            print new_filename
            os.chdir(filedir)
            os.rename(filename, new_filename)
            
        serie_id = f.split('/')[-1].split('.')[0].split('_')[-1]
        for s in ['s004', 's006', 's007']:
            if s in serie_id:
                new_filename = filename.replace(s,'s005')
                os.chdir(filedir)
                os.rename(filename, new_filename)
                print new_filename
            
    anat_path = os.path.join(BASE_DIR, subject, 'MRI', 'T1MRI')
    anat_files = glob.glob(os.path.join(anat_path, '*.*'))
    for f in anat_files:
        filedir, filename = os.path.split(f)
        filename = f.split('/')[-1]
        if 'nobias' in filename:
            new_filename = filename.replace('nobias_Exam','S')
            print new_filename
            os.chdir(filedir)
            os.rename(filename, new_filename)
        elif 'Exam' in filename:
            new_filename = filename.replace('Exam','S')
            print new_filename
            os.chdir(filedir)
            os.rename(filename, new_filename)            
            
    hdr_files = glob.glob(os.path.join(anat_path, '*.hdr'))
    if len(hdr_files)>0:
        img = nib.load(hdr_files[0])
        new_img = image.reorder_img(img,resample='continuous')
        ax = plotting.plot_img(new_img)
        ax.title(subject)


    
    