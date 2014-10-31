"""
A script that renames MID and T1MRI data :
- S[xxxxx]_s005[000i].nii
- 
"""

import os, glob

BASE_DIR = os.path.join('/', 'shfj', 'Ppsypim', 'PSYDAT', 'Subjects')

for subject in os.listdir(BASE_DIR):
    mid_path = os.path.join(BASE_DIR, subject, 'MRI', 'MID')
    mid_files = glob.glob(os.path.join(mid_path, '[a-z|A-Z]*.nii'))
    for f in mid_files:
        if 'Exam' in f:
            print f
            print f.replace('Exam','S')