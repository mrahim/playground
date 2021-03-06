# -*- coding: utf-8 -*-
"""
    A transfer script of the files of the movement regressors
    from the eprime mat folder to the MID/MAT file
"""


import os, shutil

BASE_DIR = os.path.join('/', 'home', 'mr243268', 'dev', 'playground',
                        'python', 'neuroimage', 'eprime',
                        'eprime_files', 'mat')
DST_BASE_DIR = os.path.join('/', 'home', 'Ppsypim', 'PSYDAT', 'Subjects')

for f in os.listdir(BASE_DIR):
    fpath = os.path.join(BASE_DIR, f)
    subject_id = f.split('_')[0]
    dst_dir = os.path.join(DST_BASE_DIR, subject_id, 'MRI', 'MID')
    if os.path.isdir(dst_dir):
        dst_dir = os.path.join(dst_dir, 'MAT')
        if not(os.path.isdir(dst_dir)):
            os.mkdir(dst_dir)
        shutil.copyfile(fpath, os.path.join(dst_dir, f))
        print os.path.join(dst_dir, f)