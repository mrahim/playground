"""
A script that renames MID and T1MRI data :
- S[xxxxx]_s005[000i].nii
- S[xxxxx]_struct.hdr, .img
- 
"""

import os, glob

BASE_DIR = os.path.join('/', 'home', 'Ppsypim', 'PSYDAT', 'Subjects')

for subject in os.listdir(BASE_DIR):
    mid_path = os.path.join(BASE_DIR, subject, 'MRI', 'MID')
    mid_files = glob.glob(os.path.join(mid_path, '[a-z|A-Z]*.nii'))
    for f in mid_files:
        filedir, filename = os.path.split(f)
        filename = f.split('/')[-1]
        if 'Exam' in filename:
            new_filename = filename.replace('Exam','S')
            print new_filename
            os.chdir(filedir)
            os.rename(filename, new_filename)
            
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